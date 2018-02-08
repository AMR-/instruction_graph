import uuid
from abc import ABCMeta, abstractmethod


# Users should implmenet subclasses of this, implementing list_action_primitives and
#  list_conditional_primitives which return a list of ActionPrimtives and list of ConditionalPrimitives
#  respectively, as a means of initializing
class BasePrimitiveLibrary(object):
    # A class to hold implementation-specific primitives and information (such as possible actions
    # and conditions) to use in the instruction graph

    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = self.library_name()
        print("Primitive Library initialized with name %s" % self.name)
        self.action_store = []          # Dictionary of ActionPrimitives by function Name
        self.action_raw_list = []       # List of Action Primitives
        self.condition_store = []       # Dictionary of ConditionalPrimitives by function Name
        self.condition_raw_list = []    # Lit of Condition Primitives
        self.true_lam_name = "true_lam"
        self._validate_primitives()
        self._set_action_tuples(self.list_action_primitives())
        self._set_conditional_tuples(self.list_conditional_primitives())

    def __str__(self):
        return self.library_name()

    @abstractmethod
    def library_name(self):
        return "Library_" + uuid.uuid4().hex

    @abstractmethod
    def list_action_primitives(self):
        raise NotImplementedError("Please return a list of ActionPrimitive tuples")

    @abstractmethod
    def list_conditional_primitives(self):
        raise NotImplementedError("Please return a list of ConditionalPrimitive tuples")

    # retrieve the function for this function name
    def get_action(self, fn_name):
        return self.action_store[fn_name]

    # retrieve the function for this function name
    def get_condition(self, fn_name):
        return self.condition_store[fn_name]

    # Check that provided Primitives are actually primitives.  Also checks that identifying strings are unique
    def _validate_primitives(self):
        pass  # TODO  -- check each, if type found wanting, throw an error

    # pass a list of ActionPrimitives
    def _set_action_tuples(self, action_primitive_tuples):
        self.action_raw_list = action_primitive_tuples
        self.action_store = dict(self._tuples_to_dict(action_primitive_tuples))

    # pass a list of ConditionalPrimitives
    def _set_conditional_tuples(self, conditional_primitive_tuples):
        self.condition_raw_list = conditional_primitive_tuples
        self.condition_store = dict(self._tuples_to_dict(conditional_primitive_tuples))
        self.true_lam_name = self._find_unused_fnname(self.true_lam_name, self.condition_store)
        self.condition_store[self.true_lam_name] = lambda: True

    @staticmethod
    def _tuples_to_dict(tuple_lists):
        return dict([(t.fn_name, t.function) for t in tuple_lists])

    @staticmethod
    def _find_unused_fnname(start, store):
        unused = start
        ct = 0
        while start in store:
            unused = start + str(ct)
            ct = ct + 1
        return unused
