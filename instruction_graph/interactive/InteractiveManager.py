from ..core.Manager import Manager
from ..core.IG import InstructionNode as NodeState
from .utils import synchronized_method, regex, idx_1st_match, idx_1st_true_fn
from collections import defaultdict
from enum import Enum
import traceback


class BuilderPhrases(object):
    # noinspection PySingleQuotedDocstring
    '''
        Contains the regex for matching phrases the human says to the agent, as well as creating
        the phrases that the agent will say to the human.
        
        For human input, the important inputs are
        :teach_you: - for a human to initiate the construction of a new graph.  Other responses for
        dialgoue thereafter during the construction are included as well
        :run_ig: - for a human to initaite loading and running an existing ig
        Any other response not in the middle of an interaction is construed as an instruction
            to execute a primitive, and the primitives are checked.
    '''
    def __init__(self):
        # == Human Input ==
        # For a human to initiate creating an IG
        self.CMD_GROUP = "cmd"
        self.NEG_GROUP = "neg"
        self.teach_you = regex("i will teach you to (.*)")
        self.confirm_pos = regex("y(?:es|eah)?")
        self.confirm_neg = regex("no")
        self.teaching_done = regex("done (?:learning|teaching)")
        self.h_if_cond = regex("if (?P<neg>(?:not|don'?t) )?(?P<cmd>.*)")
        self.h_while_cond = regex("(?:while|loop) (?P<neg>(?:not|don'?t) )?(?P<cmd>.*)")
        self.h_else = regex("else")
        self.h_end_if = regex("end if")
        self.h_end_loop = regex("end loop")
        self.run_ig = regex("run (.*)")

        # == Agent Responses ==
        self.agent_start = "Beginning interactive graph runner and builder."
        self.exec_prim_success = ""
        self.exec_prim_fail = "Could not find or run primitive <prim_id>"
        self.exec_prim_name_token = "<prim_id>"
        self.exec_graph_success = ""
        self.exec_graph_fail = "Could not find or run graph <prim_id>"
        self.exec_graph_name_token = "<prim_id>"
        self.build_new_graph = "I will learn to <name>?"
        self.build_new_graph_filename_token = "<name>"
        self.yes_learn = "Ok, I am ready to learn.  What is first?"
        self.no_learn = "Ok"
        self.unclear_confirm = "I don't understand. " \
                               "Can you please confirm 'yes' or 'no' please?"
        self.unclear_learn = "I don't understand. Please name a primitive to add or tell me I'm done."
        self.confirm_new_primitive = "I should <cond> <name>?"
        self.confirm_new_primitive_name_token = "<name>"
        self.confirm_new_primitive_cond_token = "<cond>"
        self.new_primitive_confirmed_pos = "Ok, what's next?"
        self.new_primitive_confirmed_neg = "Ok, what's next?"
        self.done_building_graph = "I have learned <name>."
        self.done_building_graph_filename_token = "<name>"

        self.yes = "Yes"
        self.no = "No"


class InteractiveManager(Manager):
    def __init__(self, library, memory=None, phrases=BuilderPhrases()):
        Manager.__init__(self, library, memory=memory)
        # Instruction Graph Directory - please include trailing slash
        self.ig_dir = "generated/"
        self.p = phrases
        self.state = States.WAITING

        # Learning a graph
        self.lrn_graph_name = None
        self.primitive_queued = None
        self.primitive_queued_args = None
        self.primitive_queued_neg = None
        self.primitive_queued_type = None

    def startup_greeting(self):
        return self.p.agent_start

    @synchronized_method
    def parse_input_text(self, text):
        if text and text.strip():
            return self._parse_valid_input_text(text)
        else:
            return None

    def _parse_valid_input_text(self, text):
        print("While in state %s, received text:\n%s" % (self.state, text))
        response = {
            States.WAITING: self._waiting_response,
            States.CONFIRM_LEARN_IG: self._confirm_learn_ig_response,
            States.LEARNING_IG_WAITING: self._learning_ig_waiting_response,
            States.CONFIRM_ADD_PRIM_WHEN_LEARNING: self._confirm_add_prim_when_learning_response,
        }[self.state](text)
        return response

    # :cmd_regexes: compiled regexes against which to test
    # :cmd_fns: the corresponding fn to run if match (passing the text and the Matcher).
    #   This should be of length one longer than cmd_regexes, the last is the default
    @staticmethod
    def _run_1st_match_fn(text, cmd_regexes, cmd_fns):
        match = idx_1st_match(text, cmd_regexes)
        return cmd_fns[match[0]](text, match[1] or None)

    # Will either learn a new graph, run a graph, or run a primitive
    def _waiting_response(self, text):
        cmd_regexes = [
            self.p.teach_you,
            self.p.run_ig
        ]
        cmd_fns = [
            self._from_waiting_start_learn_new_graph,
            self._from_waiting_run_graph,
            self._from_waiting_run_action_prim  # default
        ]
        return self._run_1st_match_fn(text, cmd_regexes, cmd_fns)
        # match = idx_1st_match(text, cmd_regexes)
        # return cmd_fns[match[0]](text, match[1])

    def _from_waiting_start_learn_new_graph(self, _, m):
        self.lrn_graph_name = m.group(1)
        self.state = States.CONFIRM_LEARN_IG
        return self.p.build_new_graph.replace(
            self.p.build_new_graph_filename_token, self.lrn_graph_name
        )

    def _from_waiting_run_graph(self, _, m):
        assumed_filename = self.ig_dir + m.group(1).replace(' ', '_') + ".ig"
        print("Attempting to run graph %s" % assumed_filename)
        # noinspection PyBroadException
        try:
            self.load_ig(assumed_filename)
            self.run()
            return self.p.exec_graph_success.replace(
                self.p.exec_graph_name_token, assumed_filename
            )
        except Exception:
            print(traceback.format_exc())
            return self.p.exec_graph_fail.replace(
                self.p.exec_graph_name_token, assumed_filename
            )

    def _from_waiting_run_action_prim(self, text, _):
        actions = self.library.list_action_primitives()
        cmd_functions = [a.match_regex_or_fn for a in actions]
        print("Attempting to run an action primitive signified by the input text:\n%s" % text)
        # noinspection PyBroadException
        try:
            match_id = idx_1st_true_fn(text, cmd_functions)
            action = actions[match_id]
            args = action.argparse_regex_or_fn(text)
            print("Running action with id %s" % action.fn_name)
            if action.parameterized_description:
                print("with description %s" % action.parameterized_description(args))
            action.function(self.memory_obj, *args)
            if action.parameterized_description(args):
                return "Executed %s" % action.parameterized_description(args)
            else:
                return self.p.exec_prim_success.replace(
                    self.p.exec_prim_name_token, action.fn_name
                )
        except Exception:
            print(traceback.format_exc())
            resp = self.p.exec_prim_fail.replace(
                self.p.exec_prim_name_token, text
            )
            print(resp)
            return resp

    def _confirm_learn_ig_response(self, text):
        cmd_regexes = [self.p.confirm_pos, self.p.confirm_neg]

        def pos_resp(*_):
            self.state = States.LEARNING_IG_WAITING
            self.create_new_ig()
            return self.p.yes_learn

        def neg_resp(*_):
            self.state = States.WAITING
            self.lrn_graph_name = None
            return self.p.no_learn

        cmd_fns = [pos_resp, neg_resp, lambda _, __: self.p.unclear_confirm]
        return self._run_1st_match_fn(text, cmd_regexes, cmd_fns)

    # Will either add a primitive or be done
    def _learning_ig_waiting_response(self, text):
        cmd_regexes = [
            self.p.teaching_done,
            self.p.h_if_cond,
            self.p.h_while_cond,
            self.p.h_else,
            self.p.h_end_if,
            self.p.h_end_loop
        ]
        cmd_fns = [
            self._from_learn_ig_wait_done_learn_ig,
            self._from_learn_ig_wait_add_if_cond,
            self._from_learn_ig_wait_add_while_cond,
            self._from_learn_ig_wait_add_else,
            self._from_learn_ig_wait_add_end_if,
            self._from_learn_ig_wait_add_end_loop,
            self._from_learn_ig_wait_add_action,
        ]
        return self._run_1st_match_fn(text, cmd_regexes, cmd_fns)

    def _from_learn_ig_wait_done_learn_ig(self, *_):
        filename = self.ig_dir + self.lrn_graph_name.replace(' ', '_') + ".ig"
        print("Saving IG %s" % filename)
        self.save_ig(filename)
        self.state = States.WAITING
        try:
            return self.p.done_building_graph.replace(
                self.p.done_building_graph_filename_token, self.lrn_graph_name
            )
        finally:
            self.lrn_graph_name = None

    def _from_learn_ig_wait_add_if_cond(self, _, m):
        # check if matches any conditional prims, if so try add, if not say so
        cmd = m.group(self.p.CMD_GROUP) or m.group(2)
        self.primitive_queued_neg = bool(m.group(self.p.NEG_GROUP) or m.group(1))
        prims = self.library.list_conditional_primitives()
        self.primitive_queued_type = NodeState.CONDITIONAL
        return self._queue_primitive_to_learn(cmd, prims)

    def _from_learn_ig_wait_add_while_cond(self, _, m):
        # check if matches any conditional prims, if so try add, if not say so
        cmd = m.group(self.p.CMD_GROUP) or m.group(2)
        prims = self.library.list_conditional_primitives()
        self.primitive_queued_neg = bool(m.group(self.p.NEG_GROUP) or m.group(1))
        self.primitive_queued_type = NodeState.LOOP
        return self._queue_primitive_to_learn(cmd, prims)

    def _from_learn_ig_wait_add_else(self, *_):
        self.state = States.CONFIRM_ADD_PRIM_WHEN_LEARNING
        self.primitive_queued_type = NodeState.EMPTY  # NOTE: Overloading meaning of this state here.
        return self._confirm_new_primitive("add an else clause to the if condition")

    def _from_learn_ig_wait_add_end_if(self, *_):
        self.state = States.CONFIRM_ADD_PRIM_WHEN_LEARNING
        self.primitive_queued_type = NodeState.STOP  # NOTE: Overloading meaning of this state here.
        return self._confirm_new_primitive("end the if condition")

    def _from_learn_ig_wait_add_end_loop(self, *_):
        self.state = States.CONFIRM_ADD_PRIM_WHEN_LEARNING
        self.primitive_queued_type = NodeState.ENDLOOP
        return self._confirm_new_primitive("end the loop")

    def _from_learn_ig_wait_add_action(self, text, _):
        # check if matches any prims, if so try add, if not say so
        prims = self.library.list_action_primitives()
        self.primitive_queued_type = NodeState.ACTION
        return self._queue_primitive_to_learn(text, prims)

    def _queue_primitive_to_learn(self, cmd_text, prims):
        cmd_functions = [p.match_regex_or_fn for p in prims]
        match_id = idx_1st_true_fn(cmd_text, cmd_functions)
        if match_id < len(prims):
            self.primitive_queued = prims[match_id]
            self.primitive_queued_args = self.primitive_queued.argparse_regex_or_fn(cmd_text)
            self.state = States.CONFIRM_ADD_PRIM_WHEN_LEARNING
            negation = "negated " if self.primitive_queued_neg else ""
            # noinspection PyArgumentList,Reason this_is_how_default_dict_is_supposed_to_work
            condition = defaultdict(lambda: "", {
                NodeState.LOOP: " start a while loop with %scondition " % negation,
                NodeState.CONDITIONAL: " start an if condition with %scondition " % negation
            })[self.primitive_queued_type]
            return self._confirm_new_primitive(
                self.primitive_queued.parameterized_description(self.primitive_queued_args) or
                self.primitive_queued.human_name or self.primitive_queued.fn_name,
                condition)
        else:
            return self.p.unclear_learn

    def _confirm_new_primitive(self, name, condition=""):
        return self.p.confirm_new_primitive.replace(
            self.p.confirm_new_primitive_name_token, name
        ).replace(
            self.p.confirm_new_primitive_cond_token, condition
        )

    def _confirm_add_prim_when_learning_response(self, text):
        cmd_regexes = [self.p.confirm_pos, self.p.confirm_neg]
        cmd_fns = [
            self._from_learn_ig_conf_add_prim,
            self._from_learn_ig_conf_do_not_add_prim,
            lambda _, __: self.p.unclear_confirm
        ]
        return self._run_1st_match_fn(text, cmd_regexes, cmd_fns)

    def _from_learn_ig_conf_add_prim(self, *_):
        {
            NodeState.ACTION:
                lambda: self.ig.add_action(self.primitive_queued.fn_name, args=self.primitive_queued_args),
            NodeState.CONDITIONAL:
                lambda: self.ig.add_if(self.primitive_queued.fn_name,
                                       args=self.primitive_queued_args, negation=self.primitive_queued_neg),
            NodeState.EMPTY:  # Overloaded meaning (used differently in the graph itself)
                lambda: self.ig.add_else(),
            NodeState.STOP:  # Overloaded meaning (used differently in the graph itself)
                lambda: self.ig.add_end_if(),
            NodeState.LOOP:
                lambda: self.ig.add_loop(self.primitive_queued.fn_name,
                                         args=self.primitive_queued_args, negation=self.primitive_queued_neg),
            NodeState.ENDLOOP:
                lambda: self.ig.add_end_loop(),
        }[self.primitive_queued_type]()
        self._reset_to_learn_ig_wait()
        return self.p.new_primitive_confirmed_pos

    def _from_learn_ig_conf_do_not_add_prim(self, *_):
        self._reset_to_learn_ig_wait()
        return self.p.new_primitive_confirmed_neg

    def _reset_to_learn_ig_wait(self):
        self.primitive_queued = None
        self.primitive_queued_args = None
        self.state = States.LEARNING_IG_WAITING


class States(Enum):
    WAITING = 0
    CONFIRM_LEARN_IG = 1
    LEARNING_IG_WAITING = 2
    CONFIRM_ADD_PRIM_WHEN_LEARNING = 3
