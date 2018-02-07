
class Primitive(tuple):
    def __new__(cls, fn_name, fn, human_name=None, human_description=None):
        arg_list = [fn_name, fn, human_name, human_description]
        # noinspection PyArgumentList
        return super(Primitive, cls).__new__(cls, arg_list)

    def __init__(self, fn_name, fn, human_name=None, human_description=None):
        super(Primitive, self).__init__()
        self.fn_name = fn_name                  # internal identifier for function
        self.function = fn                      # the function itself (Action returns nothing, Condition returns T/F)
        self.human_name = human_name            # (optional) human name, for use in interactives
        self.description = human_description    # (optional) human description, for use in interactives

    def __call__(self, *args, **kwargs):
        return self.function(*args)


class ActionPrimitive(Primitive):
    pass


class ConditionalPrimitive(Primitive):
    pass

#  ignore below this line...


# text_to_name - Function or regex string that returns true or matches input command
#   when it matches the Primitive
# text_to_args - Function, regex, or list.  If function, returns list of args from text.  If regex,
#   then the matching groups (in order, or by named number) denote list of args. If literal list, the
#   literal list are the args.
class MappingMixIn(object):
    def __init__(self, text_to_name, text_to_args):
        super(MappingMixIn, self).__init__()
        self.text_to_name = text_to_name
        self.text_to_args = text_to_args


# ActionPrimitiveMapper
# MappableActionPrimitive
# TODO mixes ActionPrimitive and MappingMixIn
class ActionTuple(tuple):
    def __new__(cls, fn_name_regex, fn_name, fn_args_reparse, human_name):
        return super(ActionTuple, cls).__new__(cls)
        # return tuple.__new__(ActionTuple, (regex, fn, fn_args, human_name))

    def __init__(self, fn_name_regex, fn_name, fn_args_reparse, human_name):
        super(ActionTuple, self).__init__((fn_name_regex, fn_name, fn_args_reparse, human_name))
        self.regex = fn_name_regex                  # the regex to match if the spoken phrase is this command
        self.fn = fn_name                        # the function to execute
        self.fn_args = make_fn(fn_args_reparse)     # the literal arguments for the function OR a function parse and return
        self.human_name = human_name        # the name by which robot should refer to it


class CondTuple(tuple):
    def __new__(cls, fn_name_regex, fn_name, fn_arg_reparse, human_name):
        return super(CondTuple, cls).__new__(cls)

    def __init__(self, fn_name_regex, fn, fn_arg_reparse, human_name):
        super(CondTuple, self).__init__((fn_name_regex, fn, fn_arg_reparse, human_name))
        self.regex = fn_name_regex                              # the regex to match if the spoken phrase is this command
        self.fn = fn                                    # the function to execute
        self.fn_arg_reparse = make_fn(fn_arg_reparse)   # function parse full command, returns list of args
        self.human_name = human_name                    # the name by which robot should refer to it


def make_fn(fn_or_list):
    fn = lambda: None
    return fn_or_list if isinstance(fn_or_list, type(fn)) else lambda cmd: fn_or_list

# TODO -- create the make_fn(fn_or_regex_or_list)


