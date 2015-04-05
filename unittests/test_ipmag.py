#!/usr/bin/env python

import unittest
import sys
import os
import numpy as np
import ipmag

class TestIGRF(unittest.TestCase):

    def setUp(self):
        pass
        #print 'setting up'

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
        print '!!', os.getcwd()
        self.assertFalse(outfile)
        self.assertEqual(error_message, "file validation has failed.  You may run into problems if you try to upload this file.")

    def test_with_valid_files(self):
        outfile, error_message = ipmag.upload_magic(dir_path=os.path.join(self.dir_path, 'my_project'))
        self.assertTrue(outfile)
        self.assertEqual(error_message, '')
        assert os.path.isfile(outfile)


if __name__ == '__main__':
    unittest.main()

            
