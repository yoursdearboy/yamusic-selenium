from .misc import Idable, Findable, find_or_new, \
                  LazyClass, lazyproperty, \
                  find_elements_in_scrollpane, seleniumdrived
from selenium.common.exceptions import NoSuchElementException

def find(_id):
    return find_or_new(Song, _id)

class Song(Idable, Findable, LazyClass):
    BASE = "https://music.yandex.ru/album/{artist.id}/track/{id}"

    def __init__(self, _id, title=None, album=None, artist=None, duration=None):
        self._id = _id
        self._title = title
        self._album = album
        self._artist = artist
        self._duration = duration
        self._lyrics = None

    @lazyproperty
    @seleniumdrived()
    def title(self, driver):
        return None

    @lazyproperty
    @seleniumdrived()
    def album(self, driver):
        return None

    @lazyproperty
    @seleniumdrived()
    def artist(self, driver):
        return None

    @lazyproperty
    @seleniumdrived()
    def duration(self, driver):
        return None

    @lazyproperty
    @seleniumdrived()
    def lyrics(self, driver):
        try:
            driver.find_element_by_class_name('sidebar-track__outer').find_element_by_css_selector('*').click()
            return driver.find_element_by_class_name('sidebar-track__lyric-text').text
        except NoSuchElementException:
            return None
