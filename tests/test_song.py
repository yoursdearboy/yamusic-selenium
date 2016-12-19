import unittest
from .misc import make_suite
from yamusic import Artist, Album, Song

class TestSong(unittest.TestCase):
  def __init__(self, methodName='runTest', _id=None, album_id=None, title=None, lyrics_present=None):
    super(TestSong, self).__init__(methodName)
    self.id = _id
    self.album_id = album_id
    self.title = title
    self.lyrics_present = lyrics_present

  def setUp(self):
    self.song = Song.find(self.album_id, self.id)

  def test_id(self):
    self.assertEqual(self.song.id, self.id)

  def test_title(self):
    self.assertEqual(self.song.title, self.title)

  def test_lyrics(self):
    self.assertEqual(self.song.lyrics is not None, self.lyrics_present)

def suite():
  def maker(name):
    return [
      TestSong(name, _id='30767183', album_id='3721578', title='Куртец', lyrics_present=True),
    ]
  return make_suite(TestSong, maker)
