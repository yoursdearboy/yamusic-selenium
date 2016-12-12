import queue
import threading
import atexit
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumPool(queue.Queue):
    def __init__(self, maxsize=0, driver_producer=None):
        super().__init__(maxsize)
        self._lock = threading.Lock()
        self.initsize = 0
        self.driver_producer = driver_producer
        self.driver_class = webdriver.Chrome
        self.driver_wait = 5

    @contextmanager
    def pool(self):
        driver = self.get()
        try:
            yield driver
        finally:
            self.put(driver)

    def get(self, *args):
        with self._lock:
            if self.initsize < self.maxsize and self.qsize() == 0:
                super().put(self._new_driver())
                self.initsize += 1
        return super().get(*args)

    def _new_driver(self):
        if self.driver_producer:
            return self.driver_producer()
        else:
            driver = self.driver_class()
            driver.implicitly_wait(self.driver_wait)
            atexit.register(lambda: driver.close())
            return driver
