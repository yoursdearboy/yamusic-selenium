from .misc import Idable, Findable, find_or_new, \
                  LazyClass, lazyproperty, \
                  find_elements_in_scrollpane, seleniumdriven
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def find(album_id, _id):
    song = find_or_new(Song, _id)
    song.album = Album.find(album_id)
    return song

class Song(Idable, Findable, LazyClass):
    BASE = "https://music.yandex.ru/album/{album.id}/track/{id}"

    def __init__(self, _id, title=None, album=None, artist=None, duration=None):
        self._id = _id
        self._title = title
        self._album = album
        self._artist = artist
        self._duration = duration
        self._lyrics = None

    @lazyproperty
    @seleniumdriven()
    def title(self, driver):
        return driver.find_element_by_class_name('sidebar-track__title').text

    @lazyproperty
    @seleniumdriven()
    def album(self, driver):
        raise AssertionError("Album should be set")

    @lazyproperty
    @seleniumdriven()
    def artist(self, driver):
        el = driver.find_element_by_css_selector('.album-summary > :first-child a')
        _id = el.get_attribute('href').split('/')[-1]
        title = el.get_attribute('title')
        artist = Artist.find(_id)
        artist.title = title
        return artist

    @lazyproperty
    @seleniumdriven(prefetch=False)
    def duration(self, driver):
        raise NotImplementedError()

    @lazyproperty
    @seleniumdriven()
    def lyrics(self, driver):
        try:
            driver.find_element_by_class_name('sidebar-track__outer').find_element_by_css_selector('*').click()
            return driver.find_element_by_class_name('sidebar-track__lyric-text').text
        except NoSuchElementException:
            return None

    @classmethod
    def find(clazz, album_id, _id):
        return find(album_id, _id)

from .artist import Artist
from .album import Album
