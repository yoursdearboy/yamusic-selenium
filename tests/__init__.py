import unittest
from .test_artist import suite as test_artist_suite
from .test_album import suite as test_album_suite
from .test_song import suite as test_song_suite

def suite():
  suite = unittest.TestSuite()  
  suite.addTest(test_artist_suite())
  suite.addTest(test_album_suite())
  suite.addTest(test_song_suite())
  return suite
