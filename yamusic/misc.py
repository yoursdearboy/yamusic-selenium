from . import pool, refs
from contextlib import contextmanager
from time import sleep
from string import Formatter
from functools import reduce, wraps

# Id objects
# Link them
# Find already fetched
class Idable:
    @property
    def id(self):
        return self._id

    @property
    def link(self):
        clazz = type(self)
        if clazz.BASE:
            return "%s/%s" % (clazz.BASE, self.id)
        else:
            return null

def find_or_new(clazz, _id):
    _cid = ''.join((clazz.__name__, _id))
    if _cid not in refs:
        holdref = refs[_cid] = clazz(_id)
    return refs[_cid]

class Findable:
    @classmethod
    def find(clazz, _id):
        return find_or_new(clazz, _id)

# Lazy class and properties
class LazyClass:
    def __init__(self):
        pass

    def __setattr__(self, name, value):
        private_name = name if name[0] == '_' else ''.join(('_',name))
        super(LazyClass, self).__setattr__(private_name, value)

def lazyproperty(fn):
    attr_name = '_' + fn.__name__
    @property
    def _lazyproperty(self):
        if hasattr(self, attr_name):
            value = getattr(self, attr_name)
            noncheck = value is not None
            structcheck = (type(value) is not list and type(value) is not dict) or len(value) > 0
            if noncheck and structcheck:
                return value
        value = fn(self)
        setattr(self, attr_name, value)
        return value
    return _lazyproperty

# Elements lookup in scrollpanes
SCROLL_SIZE = 20

def find_elements_in_scrollpane(driver, finder, cb, sleepn=5):
    accumulator = list()
    all_elements = set()
    while True:
        new_elements = set(finder())
        elements = list(new_elements - all_elements)
        all_elements = new_elements | all_elements
        accumulator += [cb(el) for el in elements]
        if end_of_page(driver):
            break
        scroll_by(driver, SCROLL_SIZE)
    return accumulator

def end_of_page(d):
    return d.execute_script("return document.body.scrollHeight == window.scrollY + window.innerHeight")

def scroll_by(d, n):
    d.execute_script("window.scrollBy(0,%s)" % n);

# Selenium and navigation
formater = Formatter()

def get_placeholders(tpl):
    return [t[1] for t in formater.parse(tpl)]

def seleniumdrived(url_tpl=''):
    def seleniumdrived_decorator(fn):
        @wraps(fn)
        def _seleniumdrived(self):
            clazz = type(self)
            with pool.pool() as driver:
                furl_tpl = url_tpl
                if furl_tpl[0:4] != 'http' and clazz.BASE is not None:
                    furl_tpl = ''.join((clazz.BASE, furl_tpl))
                furl_args = [ (a,reduce(getattr, a.split('.'), self)) for a in get_placeholders(furl_tpl) if a is not None]
                furl_args = dict(furl_args)
                furl = formater.format(furl_tpl, **furl_args)
                driver.get(furl)
                return fn(self, driver)
        return _seleniumdrived
    return seleniumdrived_decorator
