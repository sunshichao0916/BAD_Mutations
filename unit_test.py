#!/usr/bin/env python
import genome_jgi
import unittest
import os

class TestJGIFunctions(unittest.TestCase):

    def setUp(self):
        self.jgi_user = os.environ['jgi_user']
        self.jgi_password = os.environ['jgi_password']

    def test_user(self):
        self.assertTrue( self.jgi_user != None)
        self.assertTrue( self.jgi_password != None)

    def test_fetch_xml(self):
        jgi = genome_jgi.JGIUtils(self.jgi_user,self.jgi_password)
        #xml = genome_jgi.fetch_xml(s)
        #self.assertTrue( genome_jgi.xml != None )
        #self.assertTrue( genome_jgi.xml.find("cds") )

if __name__ == '__main__':
      unittest.main()
