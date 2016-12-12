from . import refs, pool
from .misc import find_scrollable
from .album import Album
from .song import Song

def find(_id):
    if _id in refs:
        return refs[_id]
    else:
        return Artist(_id)

class Artist:
    def __init__(self, _id, title=None, albums=[], songs=[]):
        self._id = _id
        self._title = title
        self._albums = albums
        self._songs = songs

    @property
    def title(self):
        if not self._title:
            with pool.pool() as driver:
                driver.get("https://music.yandex.ru/artist/%s" % self._id)
                self._title = driver.find_element_by_class_name('page-artist__title').text
        return self._title

    @property
    def albums(self):
        if len(self._albums) == 0:
            with pool.pool() as driver:
                driver.get("https://music.yandex.ru/artist/%s/albums" % self._id)
                aels = driver.find_elements_by_class_name('album')
                for ael in aels:
                    _id = ael.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                    title = ael.find_element_by_class_name('album__title').text
                    if _id in refs:
                        album = refs[_id]
                    else:
                        album = Album(_id, title)
                        refs[_id] = album
                    self._albums.append(album)
        return self._albums

    @property
    def songs(self):
        if len(self._songs) == 0:
            with pool.pool() as driver:
                driver.get("https://music.yandex.ru/artist/%s/tracks" % self._id)
                def process_sel(sel):
                    tnel = sel.find_element_by_class_name('track__name')
                    _id = tnel.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                    title = tnel.text
                    ael = sel.find_element_by_class_name('track__album')
                    _aid = ael.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                    atitle = ael.text
                    album = Album.find(_aid)
                    album.title = atitle
                    song = Song(_id, title, album)
                    self._songs.append(song)
                find_scrollable(driver, lambda: driver.find_elements_by_class_name('track'), process_sel)
        return self._songs

    @classmethod
    def find(clazz, _id):
        return find(_id)
