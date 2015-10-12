#!/usr/bin/env python


import urllib2
import os
import pmag
import check_updates


def get_data_model():
    """
    try to grab the up to date data model document from the EarthRef site.
    if that fails, try to get the data model document from the PmagPy directory on the user's computer.
    if that fails, return False.
    data_model is a set of nested dictionaries that looks like this:
    {'magic_contributions': 
        {'group_userid': {'data_status': 'Optional', 'data_type': 'String(10)'}, 'activate': {'data_status': 'Optional', 'data_type': 'String(1)'}, ....}, 
    'er_synthetics':
        {'synthetic_type': {'data_status': 'Required', 'data_type': 'String(50)'}, 'er_citation_names': {'data_status': 'Required', 'data_type': 'List(500)'}, ...},
    ....
    }
    the top level keys are the file types.  
    the second level keys are the possible headers for that file type.
    the third level keys are data_type and data_status for that header.
    """
    print "getting data model, please be patient"
    url = 'http://earthref.org/services/MagIC-data-model.txt'
    try:
        data = urllib2.urlopen(url)
    except urllib2.URLError:
        try:
            pmag_dir = check_updates.get_pmag_dir()
            the_file = os.path.join(pmag_dir, "/MagIC-data-model.txt")
            data = open(the_file, 'rU')
        except IOError:
            print "can't access MagIC-data-model at the moment\nif you are working offline, make sure MagIC-data-model.txt is in your PmagPy directory (or download it from https://github.com/ltauxe/PmagPy and put it in your PmagPy directory)\notherwise, check your internet connection"
            return False

    data_model = pmag.magic_read(None, data)
    ref_dicts = [d for d in data_model[0] if d['column_nmb'] != '>>>>>>>>>>']
    file_types = [d['field_name'] for d in data_model[0] if d['column_nmb'] == 'tab delimited']
    file_types.insert(0, data_model[1])
    complete_ref = {}

    dictionary = {}
    n = 0
    for d in ref_dicts:
        if d['field_name'] in file_types:
            complete_ref[file_types[n]] = dictionary
            n += 1
            dictionary = {}
        else:
            dictionary[d['field_name_oracle']] = {'data_type': d['data_type'], 'data_status': d['data_status']}
    return complete_ref


def read_upload(up_file):
    """
    take a file that should be ready for upload
    using the data model, check that all required columns are full,
    and that all numeric data is in fact numeric.
    print out warnings for any validation problems
    return True if there were no problems, otherwise return False
    """
    print "-I- Running validation for your upload file"
    f = open(up_file)
    lines = f.readlines()
    f.close()
    data = split_lines(lines)
    data_dicts = get_dicts(data)
    missing_data = {}
    number_scramble = {}
    invalid_col_names = {}
    missing_file_type = False
    data_model = get_data_model()
    reqd_file_types = ['er_locations']
    provided_file_types = set()
    if not data_model:
        return False
    for dictionary in data_dicts:
        for k, v in dictionary.items():
            if k == "file_type": # meta data
                provided_file_types.add(v)
                continue
            file_type = dictionary['file_type']
            if file_type not in data_model.keys():
                continue
            specific_data_model = data_model[file_type]

            # check if column header is in the data model
            invalid_col_name = validate_for_recognized_column(k, v, specific_data_model)
            if invalid_col_name:
                if file_type not in invalid_col_names.keys():
                    invalid_col_names[file_type] = set()
                invalid_col_names[file_type].add(invalid_col_name)
                # skip to next item, as additional validations won't work (key is not in the data model)
                continue 
            
            # make a list of missing, required data
            missing_item = validate_for_presence(k, v, specific_data_model) 
            if missing_item:
                if file_type not in missing_data.keys():
                    missing_data[file_type] = set()
                missing_data[file_type].add(missing_item)

            # make a list of data that should be numeric, but isn't
            number_fail = validate_for_numericality(k, v, specific_data_model)
            if number_fail:
                if file_type not in number_scramble.keys():
                    number_scramble[file_type] = set()
                number_scramble[file_type].add(number_fail)

    for file_type, invalid_names in invalid_col_names.items():
        print "-W- In your {} file, you are using the following unrecognized columns: {}".format(file_type, ', '.join(invalid_names))

    for file_type, wrong_cols in number_scramble.items():
        print "-W- In your {} file, you must provide only valid numbers, in the following columns: {}".format(file_type, ', '.join(wrong_cols))

    for file_type, empty_cols in missing_data.items():
        print "-W- In your {} file, you are missing data in the following required columns: {}".format(file_type, ', '.join(empty_cols))

    for file_type in reqd_file_types:
        if file_type not in provided_file_types:
            print "-W- You have not provided a(n) {} type file, which is required data".format(file_type)
            missing_file_type = True
            

    if invalid_col_names or number_scramble or missing_data or missing_file_type:
        return False
    else:
        print "-I- validation was successful"
        return True
    

def split_lines(lines):
    """
    split a MagIC upload format file into lists.
    the lists are split by the '>>>' lines between file_types.
    """
    container = []
    new_list = []
    for line in lines:
        if '>>>' in line:
            container.append(new_list)
            new_list = []
        else:
            new_list.append(line)
    container.append(new_list)
    return container
    
    
def get_dicts(data):
    """
    data must be a list of lists, from a tab delimited file.  
    in each list:
    the first list item will be the type of data.
    the second list item will be a tab delimited list of headers.
    the remaining items  will be a tab delimited list following the list of headers.
    """
    data_dictionaries = []
    for chunk in data[:-1]:
        if not chunk:
            continue
        data1 = data[0]
        file_type = chunk[0].split('\t')[1].strip('\n').strip('\r')
        keys = chunk[1].split('\t')
        clean_keys = []
        
        # remove new-line characters, and any empty string keys
        for key in keys:
            clean_key = key.strip('\n').strip('\r') 
            if clean_key:
                clean_keys.append(clean_key)
        for line in chunk[2:]:
            data_dict = {}
            for key in clean_keys:
                data_dict[key] = ""
            line = line.split('\t')
            for n, key in enumerate(clean_keys):
                data_dict[key] = line[n].strip('\n').strip('\r')
            data_dict['file_type'] = file_type
            data_dictionaries.append(data_dict)
    return data_dictionaries
        


def validate_for_recognized_column(key, value, complete_ref):
    if not key in complete_ref:
        return key
    return

        
def validate_for_presence(key, value, complete_ref):
    reqd = complete_ref[key]['data_status']
    if reqd == 'Required':
        if not value or value == " ":
            return key
    return

def validate_for_numericality(key, value, complete_ref):
    dtype = complete_ref[key]['data_type']
    if value:
        if 'Number' in dtype:
            if not isinstance(value, (int, float)):
                try:
                    float(value)
                except ValueError:
                    return key
    return
