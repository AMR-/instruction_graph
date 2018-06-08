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
                 parsed_description=lambda args: None):
        super(Primitive, self).__init__()
        self.fn_name = fn_name                   # internal identifier for function
        self.function = fn                       # the function itself (Action returns nothing, Condition returns T/F)
        self.human_name = human_name             # (optional) human name, for use in interactives
        self.description = human_description     # (optional) human description, for use in interactives

        # The function or regex used to determine if this primitive matches
        #   the input text.  str -> bool
        self.match_regex_or_fn = self._regex_or_function_to_match_function(match_re_or_fn)
        # The function or regex used to parse arguments from input text after match
        #   str -> list[str]
        self.argparse_regex_or_fn = self._regex_or_function_to_parse_function(argparse_re_or_fn)
        # The parameterized description, to describe command in a human way
        #   with the given arguments. If None, self.description should be used instead.
        #    list[str] -> str
        self.parameterized_description = parsed_description

    def __call__(self, *args, **kwargs):
        return self.function(*args)

    @staticmethod
    def _regex_or_function_to_match_function(re_or_fn):
        if isinstance(re_or_fn, type(lambda: None)):
            return re_or_fn
        elif isinstance(re_or_fn, str):
            r = re.compile(re_or_fn, flags=re.IGNORECASE)
            return lambda text: r.match(text)

    @staticmethod
    def _regex_or_function_to_parse_function(re_or_fn):
        if isinstance(re_or_fn, type(lambda: None)):
            return re_or_fn
        elif isinstance(re_or_fn, str):
            r = re.compile(re_or_fn, flags=re.IGNORECASE)
            return lambda text: list(r.match(text).groups())


class ActionPrimitive(Primitive):
    pass


class ConditionalPrimitive(Primitive):
    pass
