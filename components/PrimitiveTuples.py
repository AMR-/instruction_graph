class ActionPrimitive(tuple):
    def __new__(cls, fn_name, fn, human_name=None, human_description=None):
        # TODO investigate why this warning arises
        # noinspection PyArgumentList
        return super(ActionPrimitive, cls).__new__(cls, (fn_name, fn, human_name, human_description))

    def __init__(self, fn_name, fn, human_name=None, human_description=None):
        super(ActionPrimitive, self).__init__((fn_name, fn, human_name, human_description))
        self.fn_name = fn_name                  # internal identifier for function
        self.function = fn                      # the action function itself (returns nothing)
        self.human_name = human_name            # (optional) human name, for use in interactives
        self.description = human_description    # (optional) human description, for use in interactives

    def __call__(self, *args, **kwargs):
        return self.function(*args)


class ConditionalPrimitive(tuple):
    def __new__(cls, fn_name, fn, human_name=None, human_description=None):
        # TODO investigate why this warning arises
        # noinspection PyArgumentList
        return super(ConditionalPrimitive, cls).__new__(cls, (fn_name, fn, human_name, human_description))

    def __init__(self, fn_name, fn, human_name=None, human_description=None):
        super(ConditionalPrimitive, self).__init__((fn_name, fn, human_name, human_description))
        self.fn_name = fn_name                  # internal identifier for function
        self.function = fn                      # the condition function itself (returns T/F)
        self.human_name = human_name            # (optional) human name, for use in interactives
        self.description = human_description    # (optional) human description, for use in interactives

    def __call__(self, *args, **kwargs):
        return self.function(*args)

#  ignore below this line...

# ActionPrimitiveMapper
class ActionTuple(tuple):
    def __new__(cls, fn_name_regex, fn_name, fn_args_reparse, human_name):
        # TODO investigate why this warning arises
        # noinspection PyArgumentList
        return super(ActionTuple, cls).__new__(cls, (fn_name_regex, fn_name, fn_args_reparse, human_name))
        # return tuple.__new__(ActionTuple, (regex, fn, fn_args, human_name))

    def __init__(self, fn_name_regex, fn_name, fn_args_reparse, human_name):
        super(ActionTuple, self).__init__((fn_name_regex, fn_name, fn_args_reparse, human_name))
        self.regex = fn_name_regex                  # the regex to match if the spoken phrase is this command
        self.fn = fn_name                        # the function to execute
        self.fn_args = make_fn(fn_args_reparse)     # the literal arguments for the function OR a function parse and return
        self.human_name = human_name        # the name by which robot should refer to it


class CondTuple(tuple):
    def __new__(cls, fn_name_regex, fn_name, fn_arg_reparse, human_name):
        # noinspection PyArgumentList
        return super(CondTuple, cls).__new__(cls, (fn_name_regex, fn_name, fn_arg_reparse, human_name))

    def __init__(self, fn_name_regex, fn, fn_arg_reparse, human_name):
        super(CondTuple, self).__init__((fn_name_regex, fn, fn_arg_reparse, human_name))
        self.regex = fn_name_regex                              # the regex to match if the spoken phrase is this command
        self.fn = fn                                    # the function to execute
        self.fn_arg_reparse = make_fn(fn_arg_reparse)   # function parse full command, returns list of args
        self.human_name = human_name                    # the name by which robot should refer to it


def make_fn(fn_or_list):
    fn = lambda: None
    return fn_or_list if isinstance(fn_or_list, type(fn)) else lambda cmd: fn_or_list
