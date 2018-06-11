from InteractiveManager import InteractiveManager
from six.moves import input as py23_input


# Use text to build, edit, and view info about instruction graphs

# Commands:
# 'exit' to exit
# 'list primitives' or 'lp' to list primitives
# Anything else is considered to be a command sent to the interactive manager, see IM documentation for details
class TextCommunicator(object):
    def __init__(self, interactive_manager):
        if not isinstance(interactive_manager, InteractiveManager):
            raise ValueError("interactive_manager must extend Interactive Manager")
        self.im = interactive_manager

    def run(self):
        print("Type 'exit' to exit.  See documentation for other commands.")
        print(self.im.startup_greeting())
        cmd = self._input()
        while cmd != "exit":
            self._choose_command(cmd)
            cmd = self._input()

    def _input(self):
        # noinspection PyCompatibility, Reason-handled_by_six
        return py23_input(self._get_prompt()).lower()

    def _get_prompt(self):
        return ('' if self.im.lrn_graph_name is None else '(' + self.im.lrn_graph_name + ')') \
               + '> '

    def _choose_command(self, cmd):
        result = {
            'list primitives': self._list_primitives,
            'lp': self._list_primitives,
        }.get(cmd, self._parse_complex_command)(cmd)
        if result:
            print(result)

    # noinspection PyUnusedLocal,Reason-every_chosen-command_gets_passed_cmd
    def _list_primitives(self, cmd):
        prims = self.im.library.list_conditional_primitives() + self.im.library.list_action_primitives()
        return "\n".join([self._pretty_print_prim(p) for p in prims])

    # Interactive Manager or other complex commands
    def _parse_complex_command(self, cmd):
        return self.im.parse_input_text(cmd)

    @staticmethod
    def _pretty_print_prim(prim):
        return ': ' + (prim.human_name + " (" + prim.fn_name + ")" if prim.human_name else prim.fn_name) + \
               (("\n\t" + prim.description) if prim.description else "")
