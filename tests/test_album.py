import unittest
from .misc import make_suite
from yamusic import Artist, Album, Song

class TestAlbum(unittest.TestCase):
  def __init__(self, methodName='runTest', _id=None, title=None, artist_id=None, artist_title=None, year=None, songs_count = None):
    super(TestAlbum, self).__init__(methodName)
    self.id = _id
    self.title = title
    self.artist_id = artist_id
    self.artist_title = artist_title
    self.year = year
    self.songs_count = songs_count

  def setUp(self):
    self.album = Album.find(self.id)

  def test_id(self):
    self.assertEqual(self.album.id, self.id)

  def test_title(self):
    self.assertEqual(self.album.title, self.title)

  def test_artist(self):
    self.assertEqual(self.album.artist.id, self.artist_id)
    self.assertEqual(self.album.artist.title, self.artist_title)

  def test_year(self):
    self.assertEqual(self.album.year, self.year)

  def test_songs(self):
    self.assertEqual(len(self.album.songs), self.songs_count)
    for song in self.album.songs:
      self.assertIsInstance(song, Song)
      self.assertIsNotNone(song.title)
      self.assertIsNotNone(song.duration)
      self.assertEqual(song.album, self.album)

def suite():
  def maker(name):
    return [
      TestAlbum(name, _id='1679151', title='Three Sixty Deluxe Edition', artist_id='107953', artist_title='A Perfect Circle', year='2013', songs_count=18)
    ]
  return make_suite(TestAlbum, maker)
