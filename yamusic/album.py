from . import refs, pool

def find(_id):
    if _id in refs:
        return refs[_id]
    else:
        return Album(_id)

class Album:
    def __init__(self, _id, title=None, artist=None, year=None, songs=[]):
        self._id = _id
        self._title = title
        self._artist = artist
        self._songs = songs
        self._year = year
        refs[_id] = self

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def year(self):
        if not self._year:
            with pool.pool() as driver:
                driver.get("https://music.yandex.ru/album/%s" % self.id)
                self._year = driver.find_element_by_class_name('album-summary__group').text
        return self._year

    @property
    def link(self):
        return "https://music.yandex.ru/album/%s" % self.id

    @classmethod
    def find(clazz, _id):
        return find(_id)
