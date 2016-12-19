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
        clazz = self.__class__
        url = format_url(clazz.BASE, self)
        return url

def find_or_new(clazz, _id):
    _cid = ''.join((clazz.__name__, _id))
    if _cid not in refs:
        holdref = refs[_cid] = clazz(_id)
    return refs[_cid]

class Findable:
    @classmethod
    def find(clazz, _id):
        return find_or_new(clazz, _id)

# Links templating
formater = Formatter()

def format_url(tpl, obj):
    placeholders = [t[1] for t in formater.parse(tpl)]
    baseargs = [a.split('.')[0] for a in placeholders if a is not None]
    baseargs = [ (a, getattr(obj, a)) for a in baseargs]
    baseargs = dict(baseargs)
    url = formater.format(tpl, **baseargs)
    return url

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
    @wraps(fn)
    def _lazyproperty(self, *args, **kwargs):
        value = getattr(self, attr_name)
        noncheck = value is not None
        structcheck = (type(value) is not list and type(value) is not dict) or len(value) > 0
        if noncheck and structcheck:
            return value
        value = fn(self, *args, **kwargs)
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
def seleniumdriven(url_tpl='', prefetch=True):
    def seleniumdriven_decorator(fn):
        @wraps(fn)
        def _seleniumdriven(self, driver=None, prefetch_others=True):
            cache_mode = not prefetch_others
            clazz = self.__class__

            def visit_url(driver, tpl=url_tpl):
                if tpl[0:4] != 'http' and clazz.BASE is not None:
                    tpl = ''.join((clazz.BASE, tpl))
                url = format_url(tpl, self)
                driver.get(url)

            def do_prefetch_others(driver):
                for met_name in dir(clazz):
                    if met_name == fn.__name__:
                        continue
                    met = getattr(clazz, met_name)
                    meto = met.fget if type(met) is property else met
                    other_seleniumdriven = getattr(meto, '_seleniumdriven_prefetch', False)
                    other_url_tpl = getattr(meto, '_seleniumdriven_url_tpl', None)
                    if other_seleniumdriven and other_url_tpl == url_tpl:
                        meto(self, driver=driver, prefetch_others=False)

            def process(driver):
                if not cache_mode:
                    visit_url(driver)
                value = fn(self, driver)
                if prefetch_others:
                    do_prefetch_others(driver)

                return value

            if driver is None:
                with pool.pool() as driver:
                    return process(driver)
            else:
                return process(driver)

        if prefetch:
            setattr(_seleniumdriven, '_seleniumdriven_prefetch', True)
        setattr(_seleniumdriven, '_seleniumdriven_url_tpl', url_tpl)
        return _seleniumdriven
    return seleniumdriven_decorator
