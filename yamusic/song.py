from . import refs, pool
from selenium.common.exceptions import NoSuchElementException

class Song:
    def __init__(self, _id, title=None, album=None, artist=None, duration=None):
        self._id = _id
        self._title = title
        self._album = album
        self._artist = artist
        self._duration = duration
        self._lyrics = None

    @property
    def album(self):
        return self._album

    @property
    def title(self):
        return self._title

    @property
    def lyrics(self):
        if not self._lyrics:
            with pool.pool() as driver:
                driver.get('https://music.yandex.ru/album/%s/track/%s' % (self.album.id, self._id))
                try:
                    driver.find_element_by_class_name('sidebar-track__outer').find_element_by_css_selector('*').click()
                    self._lyrics = driver.find_element_by_class_name('sidebar-track__lyric-text').text
                except NoSuchElementException:
                    self._lyrics = None
        return self._lyrics
