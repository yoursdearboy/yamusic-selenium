from .misc import Idable, Findable, find_or_new, \
                  LazyClass, lazyproperty, \
                  find_elements_in_scrollpane, seleniumdriven

def find(_id):
    return find_or_new(Artist, _id)

class Artist(Idable, Findable, LazyClass):
    BASE = "https://music.yandex.ru/artist/{id}"

    def __init__(self, _id, title=None, albums=None, songs=None):
        self._id = _id
        self._title = title
        self._albums = albums or list()
        self._songs = songs or list()

    @lazyproperty
    @seleniumdriven()
    def title(self, driver):
        return driver.find_element_by_class_name('page-artist__title').text

    @lazyproperty
    @seleniumdriven("/albums")
    # TODO: Handle multiple artists
    def albums(self, driver):
        def process(el):
            _id = el.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
            title = el.find_element_by_class_name('album__title').text
            year = el.find_element_by_class_name('album__year').text
            year = year.split(' ')[0] if year is not None and len(year) > 0 else None
            album = Album.find(_id)
            album.title = title
            album.year = year
            album.artist = self
            return album
        return find_elements_in_scrollpane(driver, lambda: driver.find_elements_by_class_name('album'), process)

    @lazyproperty
    @seleniumdriven("/tracks")
    def songs(self, driver):
        def process(el):
            def process_album(el):
                _id = el.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                title = el.text
                album = Album.find(_id)
                album.title = title
                album.artist = self
                return album
            def process_trackname(el, album):
                _id = el.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                title = el.text
                song = Song.find(album.id, _id)
                song.title = title
                return song
            def process_trackinfo(el):
                song.duration = el.text
                return song
            album = process_album(el.find_element_by_class_name('track__album'))
            song = process_trackname(el.find_element_by_class_name('track__name'), album)
            song = process_trackinfo(el.find_element_by_class_name('track__info'))
            song.album = album
            return song
        return find_elements_in_scrollpane(driver, lambda: driver.find_elements_by_class_name('track'), process)

from .album import Album
from .song import Song
