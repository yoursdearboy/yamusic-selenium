import unittest
from .test_artist import suite as test_artist_suite
from .test_album import suite as test_album_suite

def suite():
  suite = unittest.TestSuite()  
  suite.addTest(test_artist_suite())
  suite.addTest(test_album_suite())
  return suite
