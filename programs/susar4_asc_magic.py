#!/usr/bin/env python
import sys
import pmagpy.pmag as pmag

def main():
    """
    NAME
        susar4-asc_magic.py

    DESCRIPTION
        converts ascii files generated by SUSAR ver.4.0 to MagIC formated
        files for use with PmagPy plotting software

    SYNTAX
        susar4-asc_magic.py -h [command line options]

    OPTIONS
        -h: prints the help message and quits
        -f FILE: specify .asc input file name
        -F MFILE: specify magic_measurements output file
        -Fa AFILE: specify rmag_anisotropy output file
        -Fr RFILE: specify rmag_results output file
        -Fs SFILE: specify er_specimens output file with location, sample, site, etc. information
        -usr USER: specify who made the measurements
        -loc LOC: specify location name for study 
        -ins INST: specify instrument used
        -spc SPEC: specify number of characters to specify specimen from sample
        -ncn NCON:  specify naming convention: default is #2 below
        -k15 : specify static 15 position mode - default is spinning
        -new : replace all existing magic files

    DEFAULTS
        AFILE: rmag_anisotropy.txt
        RFILE: rmag_results.txt
        SFILE: default is to create new er_specimen.txt file
        USER: ""
        LOC: "unknown"
        INST: ""
        SPEC: 0  sample name is same as site (if SPEC is 1, sample is all but last character)
        appends to  'er_specimens.txt, er_samples.txt, er_sites.txt' files
       Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site is entered under a separate column -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.
 

    """
    citation='This study'
    cont=0
    samp_con,Z="1",1
    AniRecSs,AniRecs,SpecRecs,SampRecs,SiteRecs,MeasRecs=[],[],[],[],[],[]
    user,locname,specfile="","unknown","er_specimens.txt"
    isspec,inst,specnum='0',"",0
    spin,new=1,0
    dir_path='.'
    if '-WD' in sys.argv:
        ind=sys.argv.index('-WD')
        dir_path=sys.argv[ind+1] 
    aoutput,routput,moutput=dir_path+'/rmag_anisotropy.txt',dir_path+'/rmag_results.txt',dir_path+'/magic_measurements.txt'
    if '-h' in sys.argv:
        print(main.__doc__)
        sys.exit()
    if '-usr' in sys.argv:
        ind=sys.argv.index('-usr')
        user=sys.argv[ind+1] 
    if "-ncn" in sys.argv:
        ind=sys.argv.index("-ncn")
        samp_con=sys.argv[ind+1]
        if "4" in samp_con:
            if "-" not in samp_con:
                print("option [4] must be in form 4-Z where Z is an integer")
                sys.exit()
            else:
                Z=samp_con.split("-")[1]
                samp_con="4"
        if "7" in samp_con:
            if "-" not in samp_con:
                print("option [7] must be in form 7-Z where Z is an integer")
                sys.exit()
            else:
                Z=samp_con.split("-")[1]
                samp_con="7"
    if '-k15' in sys.argv:spin=0
    if '-f' in sys.argv:
        ind=sys.argv.index('-f')
        ascfile=dir_path+'/'+sys.argv[ind+1] 
    if '-F' in sys.argv:
        ind=sys.argv.index('-F')
        moutput=dir_path+'/'+sys.argv[ind+1] 
    if '-Fa' in sys.argv:
        ind=sys.argv.index('-Fa')
        aoutput=dir_path+'/'+sys.argv[ind+1] 
    if '-Fr' in sys.argv:
        ind=sys.argv.index('-Fr')
        routput=dir_path+'/'+sys.argv[ind+1] 
    if '-Fs' in sys.argv:
        ind=sys.argv.index('-Fs')
        specfile=dir_path+'/'+sys.argv[ind+1] 
        isspec='1'
    elif '-loc' in sys.argv:
        ind=sys.argv.index('-loc')
        locname=sys.argv[ind+1] 
    if '-spc' in sys.argv:
        ind=sys.argv.index('-spc')
        specnum=-(int(sys.argv[ind+1]))
        if specnum!=0:specnum=-specnum
    if isspec=="1": 
        specs,file_type=pmag.magic_read(specfile)
    specnames,sampnames,sitenames=[],[],[]
    if '-new' not in sys.argv: # see if there are already specimen,sample, site files lying around
        try:
            SpecRecs,file_type=pmag.magic_read(dir_path+'/er_specimens.txt')
            for spec in SpecRecs:
                if spec['er_specimen_name'] not in specnames:specnames.append(samp['er_specimen_name'])
        except:
            SpecRecs,specs=[],[]
        try:
            SampRecs,file_type=pmag.magic_read(dir_path+'/er_samples.txt')
            for samp in SampRecs:
                if samp['er_sample_name'] not in sampnames:sampnames.append(samp['er_sample_name'])
        except:
            sampnames,SampRecs=[],[]
        try:
            SiteRecs,file_type=pmag.magic_read(dir_path+'/er_sites.txt')
            for site in SiteRecs:
                if site['er_site_names'] not in sitenames:sitenames.append(site['er_site_name'])
        except:
            sitenames,SiteRecs=[],[]
    try:
        input=open(ascfile,'rU')
    except:
        print('Error opening file: ', ascfile)
    Data=input.readlines()
    k=0
    while k<len(Data):
        line = Data[k]
        words=line.split()
        if "ANISOTROPY" in words: # first line of data for the spec
            MeasRec,AniRec,SpecRec,SampRec,SiteRec={},{},{},{},{}
            specname=words[0]
            AniRec['er_specimen_name']=specname
            if isspec=="1":
                for spec in specs:
                    if spec['er_specimen_name']==specname:
                        AniRec['er_sample_name']=spec['er_sample_name']
                        AniRec['er_site_name']=spec['er_site_name']
                        AniRec['er_location_name']=spec['er_location_name']
                        break
            elif isspec=="0":
                if specnum!=0:
                    sampname=specname[:specnum]
                else:
                    sampname=specname
                AniRec['er_sample_name']=sampname
		SpecRec['er_specimen_name']=specname
		SpecRec['er_sample_name']=sampname
		SampRec['er_sample_name']=sampname
		SiteRec['er_sample_name']=sampname
		SiteRec['site_description']='s'
                AniRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],samp_con,Z)
                SpecRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],samp_con,Z)
                SampRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],samp_con,Z)
                SiteRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],samp_con,Z)
                AniRec['er_location_name']=locname
                SpecRec['er_location_name']=locname
                SampRec['er_location_name']=locname
                SiteRec['er_location_name']=locname
                AniRec['er_citation_names']="This study"
                SpecRec['er_citation_names']="This study"
                SampRec['er_citation_names']="This study"
                SiteRec['er_citation_names']="This study"
            AniRec['er_citation_names']="This study"
            AniRec['magic_instrument_codes']=inst
            AniRec['magic_method_codes']="LP-X:AE-H:LP-AN-MS"
            AniRec['magic_experiment_names']=specname+":"+"LP-AN-MS"
            AniRec['er_analyst_mail_names']=user
            for key in list(AniRec.keys()):MeasRec[key]=AniRec[key]
            MeasRec['measurement_flag']='g'
            AniRec['anisotropy_flag']='g'
            MeasRec['measurement_standard']='u'
            MeasRec['measurement_description']='Bulk sucsecptibility measurement'
            AniRec['anisotropy_type']="AMS"
            AniRec['anisotropy_unit']="Normalized by trace"
            if spin==1:
                AniRec['anisotropy_n']="192"
            else:
                AniRec['anisotropy_n']="15"
        if 'Azi' in words and isspec=='0': 
            SampRec['sample_azimuth']=words[1]
            labaz=float(words[1])
        if 'Dip' in words:
            SampRec['sample_dip']='%7.1f'%(-float(words[1]))
            SpecRec['specimen_vol']='%8.3e'%(float(words[10])*1e-6) # convert actual volume to m^3 from cm^3
            labdip=float(words[1])
        if 'T1' in words and 'F1' in words: 
            k+=2 # read in fourth line down
            line=Data[k]
            rec=line.split()
            dd=rec[1].split('/')
            dip_direction=int(dd[0])+90
            SampRec['sample_bed_dip_direction']='%i'%(dip_direction)
            SampRec['sample_bed_dip']=dd[1]
            bed_dip=float(dd[1])
        if "Mean" in words:
            k+=4 # read in fourth line down
            line=Data[k]
            rec=line.split()
            MeasRec['measurement_chi_volume']=rec[1]
            sigma=.01*float(rec[2])/3.
            AniRec['anisotropy_sigma']='%7.4f'%(sigma)
            AniRec['anisotropy_unit']='SI'
        if "factors" in words:
            k+=4 # read in second line down
            line=Data[k]
            rec=line.split()
        if "Specimen" in words:  # first part of specimen data
            AniRec['anisotropy_s1']='%7.4f'%(float(words[5])/3.) # eigenvalues sum to unity - not 3
            AniRec['anisotropy_s2']='%7.4f'%(float(words[6])/3.) 
            AniRec['anisotropy_s3']='%7.4f'%(float(words[7])/3.)
            k+=1
            line=Data[k]
            rec=line.split()
            AniRec['anisotropy_s4']='%7.4f'%(float(rec[5])/3.) # eigenvalues sum to unity - not 3
            AniRec['anisotropy_s5']='%7.4f'%(float(rec[6])/3.) 
            AniRec['anisotropy_s6']='%7.4f'%(float(rec[7])/3.)
            AniRec['anisotropy_tilt_correction']='-1'
            AniRecs.append(AniRec) 
            AniRecG,AniRecT={},{}
            for key in list(AniRec.keys()):AniRecG[key]=AniRec[key]
            for key in list(AniRec.keys()):AniRecT[key]=AniRec[key]
            sbar=[]
            sbar.append(float(AniRec['anisotropy_s1']))
            sbar.append(float(AniRec['anisotropy_s2']))
            sbar.append(float(AniRec['anisotropy_s3']))
            sbar.append(float(AniRec['anisotropy_s4']))
            sbar.append(float(AniRec['anisotropy_s5']))
            sbar.append(float(AniRec['anisotropy_s6']))
            sbarg=pmag.dosgeo(sbar,labaz,labdip)
            AniRecG["anisotropy_s1"]='%12.10f'%(sbarg[0])
            AniRecG["anisotropy_s2"]='%12.10f'%(sbarg[1])
            AniRecG["anisotropy_s3"]='%12.10f'%(sbarg[2])
            AniRecG["anisotropy_s4"]='%12.10f'%(sbarg[3])
            AniRecG["anisotropy_s5"]='%12.10f'%(sbarg[4])
            AniRecG["anisotropy_s6"]='%12.10f'%(sbarg[5])
            AniRecG["anisotropy_tilt_correction"]='0'
            AniRecs.append(AniRecG)
            if bed_dip!="" and bed_dip!=0: # have tilt correction
                sbart=pmag.dostilt(sbarg,dip_direction,bed_dip)
                AniRecT["anisotropy_s1"]='%12.10f'%(sbart[0])
                AniRecT["anisotropy_s2"]='%12.10f'%(sbart[1])
                AniRecT["anisotropy_s3"]='%12.10f'%(sbart[2])
                AniRecT["anisotropy_s4"]='%12.10f'%(sbart[3])
                AniRecT["anisotropy_s5"]='%12.10f'%(sbart[4])
                AniRecT["anisotropy_s6"]='%12.10f'%(sbart[5])
                AniRecT["anisotropy_tilt_correction"]='100'
                AniRecs.append(AniRecT)
            MeasRecs.append(MeasRec) 
            if SpecRec['er_specimen_name'] not in specnames:
                SpecRecs.append(SpecRec)
                specnames.append(SpecRec['er_specimen_name'])
            if SampRec['er_sample_name'] not in sampnames:
                SampRecs.append(SampRec)
                sampnames.append(SampRec['er_sample_name'])
            if SiteRec['er_site_name'] not in sitenames:
                SiteRecs.append(SiteRec)
                sitenames.append(SiteRec['er_site_name'])
        k+=1 # skip to next specimen
    pmag.magic_write(aoutput,AniRecs,'rmag_anisotropy')
    print("anisotropy tensors put in ",aoutput)
    pmag.magic_write(moutput,MeasRecs,'magic_measurements')
    print("bulk measurements put in ",moutput)
    if isspec=="0":
        SpecOut,keys=pmag.fillkeys(SpecRecs)
        output=dir_path+"/er_specimens.txt"
        pmag.magic_write(output,SpecOut,'er_specimens')
        print("specimen info put in ",output)
        output=dir_path+"/er_samples.txt"
        SampOut,keys=pmag.fillkeys(SampRecs)
        pmag.magic_write(output,SampOut,'er_samples')
        print("sample info put in ",output)
        output=dir_path+"/er_sites.txt"
        SiteOut,keys=pmag.fillkeys(SiteRecs)
        pmag.magic_write(output,SiteOut,'er_sites')
        print("site info put in ",output)
    print(""""
         You can now import your data into the Magic Console and complete data entry, 
         for example the site locations, lithologies, etc. plotting can be done with aniso_magic.py
    """)

if __name__ == "__main__":
    main()
