"""
Test cases for the app_twitter module.
"""
from django.test import TestCase
from grandcentral.lib.common import *

class LibTest(TestCase):
    
    def test_load_url(self):
        self.assertIsNotNone( load_url("http://www.google.com") )
        self.assertIsNotNone( load_url("https://www.google.com") )
        self.assertIsNone(load_url('http://quroiuwoqiruqwoiruqwoiurqwiouroqiwuroqw.com'))
        self.assertIsNone(load_url(''))
    
    def test_is_numeric(self):
        self.assertTrue(is_numeric(u'24'))
        self.assertTrue(is_numeric(u'24.04'))
        self.assertTrue(is_numeric(u'-24'))
        self.assertTrue(is_numeric(u'-24.04'))
        
        self.assertTrue(is_numeric(u'24'), float)
        self.assertTrue(is_numeric(u'24.04'), float)
        self.assertTrue(is_numeric(u'-24'), float)
        self.assertTrue(is_numeric(u'-24.04'), float)
        
        self.assertTrue(is_numeric(u'24', int))
        self.assertTrue(is_numeric(u'24.35', int))
        
        self.assertTrue(is_numeric(u'999999999999999999999999999999999999999', long))
        self.assertTrue(is_numeric(u'-999999999999999999999999999999999999999', long))
        self.assertTrue(is_numeric(u'-999999999999999999999999999999999999999.2442', long))
        
        self.assertFalse(is_numeric(u'foo'))
        self.assertFalse(is_numeric(u'foo'), int)
        self.assertFalse(is_numeric(u'foo'), float)
        self.assertFalse(is_numeric(u'foo'), long)
        self.assertTrue(is_numeric(u'foo'), str)
        
        self.assertFalse(is_numeric(None))
        self.assertFalse(is_numeric(None, int))
        self.assertTrue(is_numeric(None, str))
        
    def test_to_integer(self):
        self.assertEquals(to_integer(u'42'), 42)
        self.assertNotEqual(to_integer(u'42.24'), 42)
        
        self.assertEquals(to_integer(u'42foobr', 99), 99)
        self.assertEquals(to_integer(u'', 99), 99)
        self.assertEquals(to_integer(1,2), 1)
        self.assertEquals(to_integer(None, 2), 2)
