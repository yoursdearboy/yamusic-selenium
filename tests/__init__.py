import unittest
from .test_artist import suite as test_artist_suite

def suite():
  suite = unittest.TestSuite()  
  suite.addTest(test_artist_suite())
  return suite
