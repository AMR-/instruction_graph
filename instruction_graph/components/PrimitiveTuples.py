import re


class Primitive(tuple):
    def __new__(cls, fn_name, fn, human_name=None, human_description=None,
                match_re_or_fn=None, argparse_re_or_fn=None,
                parsed_description=None):
        arg_list = [fn_name, fn, human_name, human_description,
                    match_re_or_fn, argparse_re_or_fn, parsed_description]
        # noinspection PyArgumentList
        return super(Primitive, cls).__new__(cls, arg_list)

    def __init__(self, fn_name, fn, human_name=None, human_description=None,
                 match_re_or_fn=lambda text: False,
                 argparse_re_or_fn=lambda text: [],
                 parsed_description=None):
        super(Primitive, self).__init__()
        self.fn_name = fn_name                   # internal identifier for function
        self.function = fn                       # the function itself (Action returns nothing, Condition returns T/F)
        self.human_name = human_name             # (optional) human name, for use in interactives
        self.description = human_description     # (optional) human description, for use in interactives

        # The function or regex used to determine if this primitive matches
        #   the input text.  str -> bool
        self.match_regex_or_fn = self._regex_or_function_to_function(match_re_or_fn)
        # The function or regex used to parse arguments from input text after match
        #   str -> list[str]
        self.argparse_regex_or_fn = self._regex_or_function_to_function(argparse_re_or_fn)
        # The parameterized description, to describe command in a human way
        #   with the given arguments. If None, self.description should be used instead.
        #    list[str] -> str
        self.parameterized_description = parsed_description

    def __call__(self, *args, **kwargs):
        return self.function(*args)

    @staticmethod
    def _regex_or_function_to_function(re_or_fn):
        if isinstance(re_or_fn, type(lambda: None)):
            return re_or_fn
        elif isinstance(re_or_fn, str):
            r = re.compile(re_or_fn, flags=re.IGNORECASE)
            return lambda text: r.match(text)


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
# class MappingMixIn(object):
#     def __init__(self, text_to_name, text_to_args):
#         super(MappingMixIn, self).__init__()
#         self.text_to_name = text_to_name
#         self.text_to_args = text_to_args
#
#
# # ActionPrimitiveMapper
# # MappableActionPrimitive
# class ActionTuple(tuple):
#     def __new__(cls, fn_name_regex, fn_name, fn_args_reparse, human_name):
#         return super(ActionTuple, cls).__new__(cls)
#         # return tuple.__new__(ActionTuple, (regex, fn, fn_args, human_name))
#
#     def __init__(self, fn_name_regex, fn_name, fn_args_reparse, human_name):
#         super(ActionTuple, self).__init__((fn_name_regex, fn_name, fn_args_reparse, human_name))
#         self.regex = fn_name_regex                  # the regex to match if the spoken phrase is this command
#         self.fn = fn_name                        # the function to execute
#         self.fn_args = make_fn(fn_args_reparse)     # the literal arguments for the function OR a function parse and return
#         self.human_name = human_name        # the name by which robot should refer to it
#
#
# class CondTuple(tuple):
#     def __new__(cls, fn_name_regex, fn_name, fn_arg_reparse, human_name):
#         return super(CondTuple, cls).__new__(cls)
#
#     def __init__(self, fn_name_regex, fn, fn_arg_reparse, human_name):
#         super(CondTuple, self).__init__((fn_name_regex, fn, fn_arg_reparse, human_name))
#         self.regex = fn_name_regex                              # the regex to match if the spoken phrase is this command
#         self.fn = fn                                    # the function to execute
#         self.fn_arg_reparse = make_fn(fn_arg_reparse)   # function parse full command, returns list of args
#         self.human_name = human_name                    # the name by which robot should refer to it
#
#
# def make_fn(fn_or_list):
#     fn = lambda: None
#     return fn_or_list if isinstance(fn_or_list, type(fn)) else lambda cmd: fn_or_list



