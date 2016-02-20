# encoding: utf-8
# Copyright (C) 2015 John Törnblom

import unittest
import tempfile
import sys
import os

import rsl


class TestCommandLineInterface(unittest.TestCase):
    
    def test_unsed_arguments(self):
        argv = ['test_unsed_arguments', 
                '-nopersist', #don't save database to disk during testing
                '-d', '1',
                '-priority', '32',
                '-lVHs', '-lSCs', '-l2b', '-l2s', '-l3b', '-l3s',
                '-e', 'some_string',
                '-t', 'some_string',
                '-v', 'STMT',
                '-q',
                '-l',
                '-#', '4']
        rsl.main(argv)

    def test_ignoring_arguments(self):
        argv = ['test_ignoring_arguments', 
                '-nopersist', #don't save database to disk during testing
                '-ignore_rest', 'some', 'more']
        rsl.main(argv)

    def test_invalid_arguments(self):
        argv = ['test_invalid_arguments', 
                'some', 'more']
        self.assertRaises(SystemExit, rsl.main, argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn('ERROR', output)
    
    def test_help(self):
        argv = ['test_help', 
                '-h']
        
        self.assertRaises(SystemExit, rsl.main, argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn('USAGE', output)
    
    def test_version(self):
        argv = ['test_version', 
                '-version']
        
        self.assertRaises(SystemExit, rsl.main, argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn(rsl.version.complete_string, output)
        
    def test_integrity(self):
        schema = tempfile.NamedTemporaryFile()
        script = tempfile.NamedTemporaryFile()
        
        schema.file.write('CREATE TABLE Cls (Id STRING);')
        schema.file.write('CREATE UNIQUE INDEX I1 ON Cls (Id);')
        schema.file.flush()
        
        script.file.write('.create object instance cls of Cls\n')
        script.file.write('.assign cls.Id = "test"\n')
        
        argv = ['test_integrity', 
                '-nopersist',
                '-integrity',
                '-import', schema.name,
                '-arch', script.name]
        
        self.assertEqual(0, rsl.main(argv))
    
        script.file.write('.create object instance cls of Cls\n')
        script.file.write('.assign cls.Id = "test"\n')
        script.file.flush()
        self.assertEqual(1, rsl.main(argv))
    
    def test_include(self):
        script = tempfile.NamedTemporaryFile()
        script.file.write('.print "Hello"\n')
        script.file.write('.include "spam.inc"\n')
        script.file.flush()
        
        argv = ['test_include', 
                '-arch', script.name,
                '-include', 
                os.path.dirname(__file__) + os.path.sep + 'test_files',
                '-nopersist']
        
        rsl.main(argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Hello', output)

    def test_nopersist(self):
        db_filename = tempfile.mktemp()
        script = tempfile.NamedTemporaryFile()

        script.file.write('.print "Hello"\n')
        script.file.flush()
        
        argv = ['test_nopersist', 
                '-f', db_filename,
                '-arch', script.name,
                '-nopersist']
        
        rsl.main(argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Hello', output)
        self.assertFalse(os.path.exists(db_filename))
    
    def test_persist(self):
        db = tempfile.NamedTemporaryFile()
        schema = tempfile.NamedTemporaryFile()
        script = tempfile.NamedTemporaryFile()
        
        schema.file.write('CREATE TABLE Cls (Id UNIQUE_ID);')
        schema.file.flush()
        
        script.file.write('.create object instance cls of Cls\n')
        script.file.write('.print "Hello"\n')
        script.file.flush()
        
        argv = ['test_persist', 
                '-f', db.name,
                '-import', schema.name,
                '-arch', script.name]
        
        rsl.main(argv)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Hello', output)
        
        with open(db.name, 'r') as f:
            s = f.read()
            self.assertIn('CREATE TABLE', s)
            self.assertIn('INSERT INTO', s)
    
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()