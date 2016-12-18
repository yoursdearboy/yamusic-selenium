import unittest
from .misc import make_suite
from yamusic import Artist, Album, Song

class TestArtist(unittest.TestCase):
  def __init__(self, methodName='runTest', _id=None, title=None, albums_count=None, songs_count=None):
    super(TestArtist, self).__init__(methodName)
    self.id = _id
    self.title = title
    self.albums_count = albums_count
    self.songs_count = songs_count

  def setUp(self):
    self.artist = Artist.find(self.id)

  def test_id(self):
    self.assertEqual(self.artist.id, self.id)

  def test_title(self):
    self.assertEqual(self.artist.title, self.title)

  def test_albums(self):
    self.assertEqual(len(self.artist.albums), self.albums_count)
    for album in self.artist.albums:
      self.assertEqual(album.artist, self.artist)
      self.assertTrue(album.year is None or album.year.isdigit())
      self.assertEqual(album.artist, self.artist)

  def test_songs(self):
    self.assertEqual(len(self.artist.songs), self.songs_count)
    for song in self.artist.songs:
      self.assertIsInstance(song, Song)
      self.assertIsNotNone(song.title)
      self.assertIsNotNone(song.duration)
      self.assertIsInstance(song.album, Album)
      self.assertIsNotNone(song.album.title)
      self.assertEqual(song.album.artist, self.artist)

def suite():
  def maker(name):
    return [
      TestArtist(name, _id='218095', title="Кровосток", albums_count=13, songs_count=66),
      TestArtist(name, _id='9278', title="Limp Bizkit", albums_count=25, songs_count=89)
    ]
  return make_suite(TestArtist, maker)
