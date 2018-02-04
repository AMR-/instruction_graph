import uuid


class ImplementationStore(object):
    # A class to hold implementation-specific information (such as possible actions
    # and condition) to use in the instruction graph

    def __init__(self, name=None):
        self.name = name if name is not None else "Imp_" + uuid.uuid4().hex
        print("Implementation Store initialized with name %s" % self.name)
        self.functionStore = []
        self.true_lam_name = "true_lam"
        self.set_fn_store(self.functionStore)

    def get(self, fn):
        return self.functionStore[fn]

    def set_fn_store(self, fn_store):
        self.functionStore = dict(fn_store)
        self.true_lam_name = self._find_unused_fnname(self.true_lam_name)
        self.functionStore[self.true_lam_name] = lambda: True

    def _find_unused_fnname(self, start):
        unused = start
        ct = 0
        while start in self.functionStore:
            unused = start + str(ct)
            ct = ct + 1
        return unused
