import threading
import re


def regex(pattern):
    return re.compile(pattern, flags=re.IGNORECASE)


# Returns the index and matcher of the first match for n regexes,
#   or the value (n+1, None) if there is no match
def idx_1st_match(text, list_of_regex):
    def rmatch(i, tex):
        return list_of_regex[i].match(tex)
    n = len(list_of_regex)
    return next(((i, rmatch(i, text)) for i in range(n) if rmatch(i, text)), (n, None))


# Returns the index of the first function to return true for :text:, or the value n+1, for n functions
def idx_1st_true_fn(text, list_of_fn):
    n = len(list_of_fn)
    return next((i for i in range(n) if list_of_fn[i](text)), n)


def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name):
                setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method
