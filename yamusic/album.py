from .misc import Idable, Findable, find_or_new, \
                  LazyClass, lazyproperty, \
                  find_elements_in_scrollpane, seleniumdrived

def find(_id):
    return find_or_new(Album, _id)

class Album(Idable, Findable, LazyClass):
    BASE = "https://music.yandex.ru/album/{id}"

    def __init__(self, _id, title=None, artist=None, year=None, songs=list()):
        self._id = _id
        self._title = title
        self._artist = artist
        self._year = year
        self._songs = songs

    @lazyproperty
    @seleniumdrived()
    def title(self, driver):
        return driver.find_element_by_class_name('album-summary__title').text

    @lazyproperty
    @seleniumdrived()
    def year(self, driver):
        return driver.find_element_by_class_name('album-summary__group').text

    @lazyproperty
    @seleniumdrived()
    def artist(self, driver):
        return None
