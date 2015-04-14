#!/usr/bin/env python

import unittest
import sys
import os
import numpy as np
import ipmag
WD = os.getcwd()

class TestIGRF(unittest.TestCase):

    def setUp(self):
        pass

    def test_igrf_output(self):
        result = ipmag.igrf([1999.1, 30, 20, 50])
        reference = [  1.20288657e+00,   2.82331112e+01,   3.9782338913649881e+04]
        for num, item in enumerate(result):
            self.assertAlmostEqual(item, reference[num])

class TestUploadMagic(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.join(os.getcwd(), 'unittests', 'examples')

    def test_empty_dir(self):
        outfile, error_message = ipmag.upload_magic(dir_path=os.path.join(self.dir_path, 'empty_dir'))
        self.assertFalse(outfile)
        self.assertEqual(error_message, "no data found, upload file not created")

    def test_with_invalid_files(self):
        outfile, error_message = ipmag.upload_magic(dir_path=os.path.join(self.dir_path, 'my_project_with_errors'))
        self.assertFalse(outfile)
        self.assertEqual(error_message, "file validation has failed.  You may run into problems if you try to upload this file.")
        directory = os.path.join(self.dir_path, 'my_project_with_errors')
        string = directory + '/' + '*.20*.txt'
        os.system('rm ' + string)

    def test_with_valid_files(self):
        print os.path.join(self.dir_path, 'my_project')
        outfile, error_message = ipmag.upload_magic(dir_path=os.path.join(self.dir_path, 'my_project'))
        self.assertTrue(outfile)
        self.assertEqual(error_message, '')
        assert os.path.isfile(outfile)
        directory = os.path.join(self.dir_path, 'my_project_with_errors')
        os.system('rm {}'.format(os.path.join(directory, outfile)))


class TestODP_samples_magic(unittest.TestCase):

    def setUp(self):
        self.input_dir = os.path.join(WD, 'Datafiles', 'Measurement_Import', 'IODP_csv_magic')

    def tearDown(self):
        os.chdir(WD)
        if os.path.isfile('./er_samples.txt'):
            os.system('rm er_samples.txt')
        
    def test_with_wrong_format(self):
        infile = os.path.join(self.input_dir, 'GCR_U1359_B_coresummary.csv')
        program_ran, error_message = ipmag.ODP_samples_magic(infile)
        self.assertFalse(program_ran)
        expected_error = 'Could not extract the necessary data from your input file.\nPlease make sure you are providing a correctly formated ODP samples csv file.'
        self.assertEqual(error_message, expected_error)


    def test_with_right_format(self):
        reference_file = os.path.join(WD, 'unittests', 'examples', 'ODP_magic_er_samples.txt')
        infile = os.path.join(self.input_dir, 'samples_318_U1359_B.csv')
        program_ran, outfile = ipmag.ODP_samples_magic(infile)
        self.assertTrue(program_ran)
        self.assertEqual(outfile, './er_samples.txt')
        self.assertTrue(os.path.isfile(outfile))


    def test_content_with_right_format(self):
        reference_file = os.path.join(WD, 'unittests', 'examples', 'ODP_magic_er_samples.txt')
        infile = os.path.join(self.input_dir, 'samples_318_U1359_B.csv')
        program_ran, outfile = ipmag.ODP_samples_magic(infile)
        self.assertEqual(open(reference_file).readlines(), open(outfile).readlines())
        
        

    

if __name__ == '__main__':
    unittest.main()

            
