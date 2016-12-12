from weakref import WeakValueDictionary
refs = WeakValueDictionary()

from .selenium_pool import SeleniumPool
pool = SeleniumPool(3)

from .artist import Artist
from .song import Song
from .album import Album
