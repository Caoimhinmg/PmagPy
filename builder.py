#!/usr/bin/env python

"""
Not empty
"""

import os
import pmag
import validate_upload

class ErMagicBuilder(object):
    """
    more object oriented builder
    """

    def __init__(self, WD):
        self.WD = WD
        self.specimens = []
        self.samples = []
        self.sites = []
        self.locations = []
        self.data_model = validate_upload.get_data_model()


    def find_by_name(self, item_name, items_list):
        """
        Return item from items_list with name item_name.
        """
        names = [item.name for item in items_list]
        if item_name in names:
            ind = names.index(item_name)
            return items_list[ind]
        return False

    def change_specimen(self, old_spec_name, new_spec_name, new_sample_name=None, new_specimen_data={}):
        """
        Find actual data objects for specimen and sample.
        Then call specimen class change method. 
        """
        specimen = self.find_by_name(old_spec_name, self.specimens)
        if not specimen:
            print '-W- {} is not a currently existing specimen, so cannot be updated'.format(spec_name)
            return False
        if new_sample_name:
            new_sample = self.find_by_name(new_sample_name, self.samples)
            if not new_sample:
                print "-W- {} is not a currently existing sample.\nLeaving sample unchanged as: {} for {}".format(new_sample_name, specimen.sample or '*empty*', specimen)
        else:
            new_sample = None
        specimen.change_specimen(new_spec_name, new_sample, new_specimen_data)

    def delete_specimen(self, spec_name):
        specimen = self.find_by_name(spec_name, self.specimens)
        sample = specimen.sample
        if sample:
            sample.specimens.remove(specimen)
        self.specimens.remove(specimen)
        del specimen

    def add_specimen(self, spec_name, samp_name=None, spec_data={}):
        sample = self.find_by_name(samp_name, self.samples)
        specimen = Specimen(spec_name, sample, self.data_model, spec_data)
        self.specimens.append(specimen)
        if sample:
            sample.specimens.append(specimen)
        return specimen

    def change_sample(self, old_samp_name, new_samp_name, new_site_name=None, new_sample_data={}):
        sample = self.find_by_name(old_samp_name, self.samples)
        if not sample:
            print '-W- {} is not a currently existing sample'.format(old_samp_name)
            return False
        if new_site_name:
            new_site = self.find_by_name(new_site_name, self.sites)
            if not new_site:
                print "-W- {} is not a currently existing site.\nLeaving site unchanged as: {} for {}".format(new_site_name, sample.site or '*empty*', sample)
                new_site = None
        else:
            new_site = None
        sample.change_sample(new_samp_name, new_site, new_sample_data)
        for spec in sample.specimens:
            spec.sample = ''

    def add_sample(self, samp_name, site_name=None, samp_data={}):
        site = self.find_by_name(site_name, self.sites)
        sample = Sample(samp_name, site, self.data_model, samp_data)
        self.samples.append(sample)
        if site:
            site.samples.append(sample)
        return sample
            

    def delete_sample(self, sample_name, replacement_samp=None):
        sample = self.find_by_name(sample_name, self.samples)
        specimens = sample.specimens
        site = sample.site
        if site:
            site.samples.remove(sample)
        self.samples.remove(sample)
        for spec in specimens:
            spec.sample = ""


    def change_site(self, old_site_name, new_site_name, new_location_name=None, new_site_data={}):
        pass

    def add_site(self, site_name, location_name=None, site_data={}):
        pass
    
    def delete_site(self, site_name, replacement_site=None):
        pass

    def change_location(self, location, new_name, new_site_data={}):
        pass
        
    #def find_all_children(self, parent_item):
    #    """
    #
    #    ancestry = ['specimen', 'sample', 'site', 'location']
    #    child_types = {'sample': self.specimens, 'site': self.samples, 'location': self.sites}
    #    dtype = parent_item.dtype
    #    ind = ancestry.index(dtype)
    #    children = child_types[dtype]
    #
    #    if dtype in (1, 2, 3):
    #        pass


    def get_data(self):
        """
        attempt to read measurements file in working directory.
        """
        try:
            meas_data, file_type = pmag.magic_read(os.path.join(self.WD, "magic_measurements.txt"))
        except IOError:
            print "-E- ERROR: Can't find magic_measurements.txt file. Check path."
            return {}
        if file_type == 'bad_file':
            print "-E- ERROR: Can't read magic_measurements.txt file. File is corrupted."

        for rec in meas_data:
            #print 'rec', rec
            specimen_name = rec["er_specimen_name"]
            if specimen_name == "" or specimen_name == " ":
                continue
            sample_name = rec["er_sample_name"]
            site_name = rec["er_site_name"]
            location_name = rec["er_location_name"]

            # add items and parents
            location = self.find_by_name(location_name, self.locations)
            if not location:
                location = Location(location_name, self.data_model)
                self.locations.append(location)
            site = self.find_by_name(site_name, self.sites)
            if not site:
                site = Site(site_name, location, self.data_model)
                self.sites.append(site)
            sample = self.find_by_name(sample_name, self.samples)
            if not sample:
                sample = Sample(sample_name, site, self.data_model)
                self.samples.append(sample)
            specimen = self.find_by_name(specimen_name, self.specimens)
            if not specimen:
                specimen = Specimen(specimen_name, sample, self.data_model)
                self.specimens.append(specimen)

            # add child_items
            if not self.find_by_name(specimen_name, sample.specimens):
                sample.specimens.append(specimen)
            if not self.find_by_name(sample_name, site.samples):
                site.samples.append(sample)
            if not self.find_by_name(site_name, location.sites):
                location.sites.append(site)


class Pmag_object(object):
    """
    Base class for Specimens, Samples, Sites, etc.
    """

    def __init__(self, name, dtype, data_model=None, data={}):#, headers={}):
        if not data_model:
            self.data_model = validate_upload.get_data_model()
        else:
            self.data_model = data_model
        self.name = name
        self.dtype = dtype

        er_name = 'er_' + dtype + 's'
        pmag_name = 'pmag_' + dtype + 's'
        self.pmag_reqd_headers, self.pmag_optional_headers = self.get_headers(pmag_name)
        self.er_reqd_headers, self.er_optional_headers = self.get_headers(er_name)
        reqd_data = {key: '' for key in self.er_reqd_headers}
        if data:
            self.data = self.combine_dicts(data, reqd_data)
        else:
            self.data = reqd_data

        self.remove_headers()

        #if headers:
        #    self.headers = self.combine_dicts(headers, 

        #
        
        #def combine_dicts(self, new_dict, old_dict):
        #"""
        #returns a dictionary with all key, value pairs from new_dict.
        #also returns key, value pairs from old_dict, if that key does not exist in new_dict.
        #if a key is present in both new_dict and old_dict, the new_dict value will take precedence.
        #"""


    def __repr__(self):
        return self.dtype + ": " + self.name

    def get_headers(self, data_type):
        """
        If data model not present, get data model from Earthref site or PmagPy directory.
        Return a list of required headers and optional headers for given data type.
        """
        try:
            data_dict = self.data_model[data_type]
        except KeyError:
            return [], []
        reqd_headers = sorted([header for header in data_dict.keys() if data_dict[header]['data_status'] == 'Required'])
        optional_headers = sorted([header for header in data_dict.keys() if data_dict[header]['data_status'] != 'Required'])
        return reqd_headers, optional_headers

    def remove_headers(self):
        for header in ['er_specimen_name', 'er_sample_name', 'er_site_name', 'er_location_name']:
            if header in self.data.keys():
                self.data.pop(header)

    def combine_dicts(self, new_dict, old_dict):
        """
        returns a dictionary with all key, value pairs from new_dict.
        also returns key, value pairs from old_dict, if that key does not exist in new_dict.
        if a key is present in both new_dict and old_dict, the new_dict value will take precedence.
        """
        old_data_keys = old_dict.keys()
        new_data_keys = new_dict.keys()
        all_keys = set(old_data_keys).union(new_data_keys)
        combined_data_dict = {}
        for k in all_keys:
            try:
                combined_data_dict[k] = new_dict[k]
            except KeyError:
                combined_data_dict[k] = old_dict[k]
        return combined_data_dict





class Specimen(Pmag_object):

    """
    Specimen level object
    """
    def __init__(self, name, sample, data_model=None, data={}):
        dtype = 'specimen'
        super(Specimen, self).__init__(name, dtype, data_model, data)
        self.sample = sample or ""


    def change_specimen(self, new_name, new_sample=None, data_dict=None):
        self.name = new_name
        if new_sample:
            self.sample.specimens.remove(self)
            self.sample = new_sample
            self.sample.specimens.append(self)
        if data_dict:
            self.data = self.combine_dicts(data_dict, self.data)

            

class Sample(Pmag_object):

    """
    Sample level object
    """

    def __init__(self, name, site, data_model=None, site_data={}):
        dtype = 'sample'
        super(Sample, self).__init__(name, dtype, data_model, site_data)
        self.specimens = []
        self.site = site or ""

    def change_sample(self, new_name, new_site=None, data_dict=None):
        self.name = new_name
        if new_site:
            if self.site:
                self.site.samples.remove(self)
            self.site = new_site
            self.site.samples.append(self)
        if data_dict:
            self.data = self.combine_dicts(data_dict, self.data)




class Site(Pmag_object):

    """
    Site level object
    """

    def __init__(self, name, location, data_model=None):
        dtype = 'site'
        super(Site, self).__init__(name, dtype, data_model)
        self.samples = []
        self.location = location or ""

    def change_site(self, new_name, new_location=None, data_dict=None):

        # maybe make this a Pmag_object method
        self.name = new_name
        if new_location:
            self.location = new_location
        if data_dict:
            self.combine_dicts(data_dict, self.data)



class Location(Pmag_object):

    """
    Location level object
    """

    def __init__(self, name, data_model=None):
        dtype = 'location'
        super(Location, self).__init__(name, dtype, data_model)
        self.sites = []
        self.data = {}

    def change_location(self, new_name, data_dict=None):
        self.name = new_name
        if data_dict:
            self.combine_dicts(data_dict, self.data)





if __name__ == '__main__':
    wd = pmag.get_named_arg_from_sys('-WD', default_val=os.getcwd())
    builder = ErMagicBuilder(wd)
    builder.get_data()
    #specimen = Specimen('spec1', 'specimen')
    #for spec in builder.specimens:
        #print str(spec) + ' belongs to ' + str(spec.sample) + ' belongs to ' + str(spec.sample.site) + ' belongs to ' + str(spec.sample.site.location)
    for site in builder.sites:
        print site, site.samples
        print '--'
