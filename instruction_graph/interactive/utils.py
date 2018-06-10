import threading
# import sys
import re


# def py_version():
#     return sys.version_info.major

# if py_version() == 2:
#     pass # TODO
# else:
#     import importlib.util as ilu


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


# def load_class_from_file(filepath, modulename, classname, args=None):
#     if py_version() == 3:  # python 3
#         spec = ilu.spec_from_file_location(modulename, filepath)
#         foo = ilu.module_from_spec(spec)
#         spec.loader.exec_module(foo)
#         return foo.MyClass(args) if args else foo.MyClass()  # TODO
#     elif py_version() == 2:
#         pass
#         TODO
    # else:
    #     return NotImplementedError()


# cpath of the form 'instruction_graph.example.ExamplePrimitiveLibrary.ExamplePrimitiveLibrary'
# def import_class_from_loaded_module(cpath):
#     components = cpath.split('.')
#     mod = __import__(components[0])
#     for comp in components[1:]:
#         mod = getattr(mod, comp)
#     return mod
