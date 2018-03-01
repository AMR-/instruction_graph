from __future__ import absolute_import
import klepto
import time
from .IG import IG
from .IG import InstructionNode
from operator import xor


class Manager:
    # library - pass an instance of a class that extends BasePrimitiveLibrary
    # memory - optionally, include a memory (instance of a class that extends BaseMemory)
    def __init__(self, library, memory=None):
        print("Behavior Manager initialized")
        # TODO validate that library and memory are sublcassing the appropriate base objects
        self.ig = None  # TODO don't force ppl to refer to the ig directly, give convenience methods in the Manager
        self.ig_key = 'instruction_graph'
        self.library = library
        self.memory_obj = memory
        print("Robot is initialized with library %s and memory object %s." % (self.library, self.memory_obj))

    def reset_init(self, library, memory=None):
        self.ig = None
        self.library = library
        self.memory_obj = memory
        print("Robot is reset with library %s and memory object %s." % (self.library, self.memory_obj))

    def create_new_ig(self):
        self.ig = IG()

    def save_ig(self, file_name):
        print("Attempting to save %s" % file_name)
        ig_file = self.get_ig_file(file_name)
        ig_file[self.ig_key] = self.ig
        ig_file.dump()
        print("Behavior is saved to ", file_name)

    def load_ig(self, file_name):
        ig_file = self.get_ig_file(file_name)
        ig_file.load()
        self.ig = ig_file[self.ig_key]
        self.ig.reset()
        print("Behavior ", file_name, " is loaded")

    @staticmethod
    def get_ig_file(file_name):
        return klepto.archives.file_archive(file_name, serialized=True)

    def run(self):
        self.ig.reset()
        while self._step():
            pass

    def _step(self):
        if self.ig.currentNode is not None:
            self._execute_current_node()
            return True
        else:
            print("end of execution")
            return False

    def _execute_current_node(self):
        print("executing step ", self.ig.currentNode.type_str(),
              self.ig.currentNode.Fn, self.ig.currentNode.FnArgs,
              "Negation is %s" % self.ig.currentNode.c_not if self.ig.currentNode.takes_conditional_primitive()
              else "[not conditional]")
        print(self.ig.currentNode.neighbors)
        if self.ig.currentNode.type == InstructionNode.ACTION:
            self._execute_action_node()
        elif self.ig.currentNode.type == InstructionNode.LOOP:
            self._execute_loop_node()
        elif self.ig.currentNode.type == InstructionNode.CONDITIONAL:
            self._execute_if_condition_node()
        elif self.ig.currentNode.type == InstructionNode.ENDLOOP:
            self._execute_end_loop_node()
        else:
            print("node type: %s" % self.ig.currentNode.type)
            self._next_node()

    def _execute_action_node(self):
        print("executing action ")
        if self.ig.currentNode.useMemory:
            self.library.get_action(self.ig.currentNode.Fn)(
                self.memory_obj, *self.ig.currentNode.FnArgs
            )
        else:
            self.library.get_action(self.ig.currentNode.Fn)(
                *self.ig.currentNode.FnArgs
            )
        time.sleep(1)
        self._next_node()

    def _execute_loop_node(self):
        print("checking loop condition %s" % self.ig.currentNode.Fn)
        cond = self._check_condition_as_requested_by_node(self.ig.currentNode)
        if cond:
            print("condition true, continuing the loop")
            self._next_node()
        else:
            print("condition false, exiting the loop")
            if len(self.ig.currentNode.neighbors[1].neighbors) > 1:
                self.ig.currentNode = self.ig.currentNode.neighbors[1].neighbors[1]
            else:
                self.ig.currentNode = None

    def _execute_end_loop_node(self):
        print("endloop node")
        self._next_node()

    def _execute_if_condition_node(self):
        print("checking if condition")
        cond = self._check_condition_as_requested_by_node(self.ig.currentNode)
        if cond:
            print("if condition true")
            self.ig.currentNode = self.ig.currentNode.neighbors[0]
        else:
            print("if condition false")
            self.ig.currentNode = self.ig.currentNode.neighbors[1]

    # Checks the condition that is on the node, and if the NOT boolean is set, flips it
    def _check_condition_as_requested_by_node(self, node):
        if node.c_not:
            print("(Negation is in effect on this node.)")
        return xor(self._check_condition(node), node.c_not)

    def _check_condition(self, node):
        if node.useMemory:
            condition_result = self.library.get_condition(node.Fn)(
                self.memory_obj, *node.FnArgs
            )
        else:
            condition_result = self.library.get_condition(node.Fn)(
                *node.FnArgs
            )
        return condition_result

    def _next_node(self):
        if len(self.ig.currentNode.neighbors) > 0:
            self.ig.currentNode = self.ig.currentNode.neighbors[0]
        else:
            self.ig.currentNode = None
