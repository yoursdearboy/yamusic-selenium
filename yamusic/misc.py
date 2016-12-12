from contextlib import contextmanager

@contextmanager
def find_scrollable(driver, finder, cb):
    all_elements = []
    while True:
        new_elements = finder()
        rly_new_elements = list(set(new_elements) - set(all_elements))
        if len(rly_new_elements) == 0:
            break
        else:
            all_elements += rly_new_elements
            for el in rly_new_elements:
                cb(el)
            scroll_to(driver, rly_new_elements[-1])

def scroll_to(d, el):
    d.execute_script("return arguments[0].scrollIntoView();", el)
