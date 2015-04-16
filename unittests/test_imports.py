#!/usr/bin/env python

import unittest
import sys
import os
import numpy as np
import ipmag
import sio_magic
import CIT_magic
import IODP_csv_magic
import old_IODP_csv_magic
import IODP_jr6_magic
WD = os.getcwd()

class TestSIO_magic(unittest.TestCase):

    def setUp(self):
        os.chdir(WD)

    def tearDown(self):
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        if os.path.isfile(meas_file):
            os.system('rm {}'.format(meas_file))

    def test_SIO_magic_no_files(self):
        program_ran, error_message = sio_magic.main(False)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, 'mag_file field is required option')
        
    def test_SIO_magic_success(self):
        options = {}
        options['mag_file'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.dat')
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        options['meas_file'] = meas_file
        program_ran, file_name = sio_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(file_name, meas_file)

    def test_SIO_magic_fail_option4(self):
        options = {}
        options['mag_file'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.dat')
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        options['meas_file'] = meas_file
        options['samp_con'] = '4'
        program_ran, error_message = sio_magic.main(False, **options)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, "naming convention option [4] must be in form 4-Z where Z is an integer")

    def test_SIO_magic_succeed_option4(self):
        options = {}
        options['mag_file'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.dat')
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        options['meas_file'] = meas_file
        options['samp_con'] = '4-2'
        program_ran, file_name = sio_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(file_name, meas_file)


    def test_SIO_magic_fail_with_coil(self):
        options = {}
        options['mag_file'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.dat')
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        options['meas_file'] = meas_file
        options['coil'] = 4
        program_ran, error_message = sio_magic.main(False, **options)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, '4 is not a valid coil specification')

    def test_SIO_magic_succeed_with_coil(self):
        options = {}
        options['mag_file'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.dat')
        meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        options['meas_file'] = meas_file
        options['coil'] = '1'
        program_ran, file_name = sio_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(file_name, meas_file)


class TestCIT_magic(unittest.TestCase):

    def setUp(self):
        os.chdir(WD)

    def tearDown(self):
        for f in ['magic_measurements.txt', 'er_specimens.txt', 'er_samples.txt', 'er_sites.txt']:
            full_file = os.path.join(WD, f)
            if os.path.isfile(full_file):
                os.system('rm {}'.format(full_file))

    def test_CIT_with_no_files(self):
        program_ran, error_message = CIT_magic.main(False)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, 'bad sam file name')

    def test_CIT_magic_with_file(self):
        options = {}
        options['input_dir_path'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'CIT_magic', 'MP18')
        options['magfile'] = 'bMP.sam'
        program_ran, outfile = CIT_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './magic_measurements.txt')

    def test_CIT_magic_fail_option4(self):
        options = {}
        options['input_dir_path'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'CIT_magic', 'MP18')
        options['magfile'] = 'bMP.sam'
        options['samp_con'] = '4'
        program_ran, error_message = CIT_magic.main(False, **options)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, "naming convention option [4] must be in form 4-Z where Z is an integer")

    def test_CIT_magic_succeed_option4(self):
        options = {}
        options['input_dir_path'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'CIT_magic', 'MP18')
        options['magfile'] = 'bMP.sam'
        options['samp_con'] = '4-3'
        program_ran, outfile = CIT_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './magic_measurements.txt')

    def test_CIT_magic_with_options(self):
        options = {}
        options['input_dir_path'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'CIT_magic', 'MP18')
        options['magfile'] = 'bMP.sam'
        options['samp_con'] = '2'
        options['methods'] = ['SO-SM:SO-MAG']
        options['locname'] = 'location'
        options['avg'] = 1
        options['specnum'] = 2
        program_ran, outfile = CIT_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './magic_measurements.txt')

    def test_CIT_magic_with_other_data(self):
        options = {}
        options['input_dir_path'] = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'CIT_magic', 'Z35')
        options['magfile'] = 'Z35.sam'
        options['samp_con'] = '1'
        options['methods'] = ['SO-SM:SO-MAG']
        options['locname'] = 'location'
        options['avg'] = 1
        options['specnum'] = 2
        program_ran, outfile = CIT_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './magic_measurements.txt')

        
class TestIODP_csv_magic(unittest.TestCase):

    def setUp(self):
        os.chdir(WD)

    def tearDown(self):
        pass
        #meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        #if os.path.isfile(meas_file):
        #    os.system('rm {}'.format(meas_file))


    def test_IODP_with_no_files(self):
        program_ran, error_message = IODP_csv_magic.main(False)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, 'No .csv files were found')

    @unittest.skip("IODP_csv_magic is missing an example datafile")
    def test_IODP_with_files(self):
        options = {}
        dir_path = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_csv_magic')
        options['dir_path'] = dir_path
        program_ran, outfile = IODP_csv_magic.main(False, **options)
        self.assertTrue(program_ran)

    @unittest.skip("IODP_csv_magic is missing an example datafile")
    def test_IODP_with_one_file(self):
        options = {}
        dir_path = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_csv_magic')
        options['input_dir_path'] = dir_path
        options['csv_file'] = 'SRM_318_U1359_B_A.csv'
        program_ran, outfile = IODP_csv_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, os.path.join(dir_path, 'SRM_318_U1359_B_A.csv.magic'))


class Test_old_IODP_csv_magic(unittest.TestCase):

    def setUp(self):
        os.chdir(WD)

    def tearDown(self):
        for f in ['magic_measurements.txt', 'er_specimens.txt', 'er_samples.txt', 'er_sites.txt', 'SRM_318_U1359_B_A.csv.magic']:
            full_file = os.path.join(WD, f)
            if os.path.isfile(full_file):
                os.system('rm {}'.format(full_file))
        #meas_file = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'sio_magic', 'sio_af_example.magic')
        #if os.path.isfile(meas_file):
        #    os.system('rm {}'.format(meas_file))


    def test_old_IODP_with_no_files(self):
        program_ran, error_message = old_IODP_csv_magic.main(False)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, 'No .csv files were found')

    def test_old_IODP_with_files(self):
        options = {}
        dir_path = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_csv_magic')
        options['input_dir_path'] = dir_path
        program_ran, outfile = old_IODP_csv_magic.main(False, **options)
        self.assertTrue(program_ran)

    def test_old_IODP_with_one_file(self):
        options = {}
        input_dir_path = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_csv_magic')
        options['input_dir_path'] = input_dir_path
        options['csv_file'] = 'SRM_318_U1359_B_A.csv'
        options['meas_file'] = 'SRM_318_U1359_B_A.csv.magic'
        program_ran, outfile = old_IODP_csv_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './SRM_318_U1359_B_A.csv.magic')

        
class TestIODP_jr6_magic(unittest.TestCase):

    def setUp(self):
        os.chdir(WD)

    def tearDown(self):
        input_dir = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_jr6_magic')
        files = ['test.magic', 'other_er_samples.txt']
        for f in files:
            full_file = os.path.join(WD, f)
            if os.path.isfile(full_file):
                os.system('rm {}'.format(full_file))

    def test_IODP_jr6_with_no_files(self):
        options = {}
        program_ran, error_message = IODP_jr6_magic.main(False, **options)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, "You must provide an IODP_jr6 format file")

    def test_IODP_jr6_with_magfile(self):
        options = {}
        input_dir = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_jr6_magic')
        options['input_dir_path'] = input_dir
        mag_file = 'test.jr6'
        options['mag_file'] = 'test.jr6'
        meas_file = 'test.magic'
        options['meas_file'] = meas_file
        program_ran, outfile = IODP_jr6_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, os.path.join('.', meas_file))
        
    def test_IODP_jr6_with_options(self):

        options = {}
        input_dir = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_jr6_magic')
        options['input_dir_path'] = input_dir
        mag_file = 'test.jr6'
        options['mag_file'] = 'test.jr6'
        meas_file = 'test.magic'
        options['meas_file'] = meas_file
        options['noave'] = 1
        program_ran, outfile = IODP_jr6_magic.main(False, **options)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, os.path.join('.', meas_file))


    def test_IODP_jr6_with_magfile_but_hidden_sampfile(self):
        options = {}
        input_dir = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_jr6_magic')
        samp_file = os.path.join(input_dir, 'er_samples.txt')
        hidden_samp_file = os.path.join(input_dir, 'hidden_er_samples.txt')
        os.system('mv {} {}'.format(samp_file, hidden_samp_file))
        options['input_dir_path'] = input_dir
        mag_file = 'test.jr6'
        options['mag_file'] = mag_file
        program_ran, error_message = IODP_jr6_magic.main(False, **options)
        msg = "Your input directory:\n{}\nmust contain an er_samples.txt file".format(input_dir)
        self.assertFalse(program_ran)
        self.assertEqual(error_message, msg)
        os.system('mv {} {}'.format(hidden_samp_file, samp_file))



