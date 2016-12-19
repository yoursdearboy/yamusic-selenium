# Yandex Music navigator (using Selenium)

Allows navigating and parsing Yandex Music using Selenium. **No support (and won't be) for downloading!!**

There is 3 modules: `artist`, `album`, `song`. Each has a so named class and all they are in the root of the package. Modules and classes has `find(id)` method, except Song that requires two arguments: `find(album_id, id)`.

Data are accessible using lazy-loading properties. List of implemented props:

* Artist: `title` `albums` `songs`
* Album: `title` `year` `songs`
* Song: `title` `album` `artist` `duration` `lyrics`

A lot of data is missing. Look at source code of main classes. It's fairly easy to write what you may need.

**Tested with Chrome. Probably won't work with unusual browsers (e.g. PhantomJS).**

**Also, it seems that tracklists and albums aren't working if window isn't visible (at least a small corner).**

## Installation

`pip install git+https://github.com/yoursdearboy/yamusic-selenium.git` or

```
git clone https://github.com/yoursdearboy/yamusic-selenium.git
cd yamusic-selenium
python setup.py install
```

You may want to run tests first `python -m unittest tests.suite`

## Example

```
from yamusic import artist
a = artist.find('218095')
print(a.title)

from yamusic import Album
# or
# from yamusic.album import Album
a = Album.find('1679151')
for s in a.songs:
  print(s.lyrics)
```

## Multithreading and driver configuration

You can run multiple driver instances. There is a pool of them in the root of the package named `pool`. It initializes drivers on demand, so you can configure driver before:

```
from yamusic import pool

pool.maxsize = 5 # Max number of working drivers
pool.driver_class = webdriver.Chrome # Driver's class to instantiate
pool.driver_wait = 5 # Time to wait for element before raising NoSuchElementException
pool.driver_producer = lambda: # Used if is not None. Custom method to create new driver. Close at exit and set waits yourself.
```
