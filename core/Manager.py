import pickle
import time

import IG
from IG import InstructionNode


class Manager:
    # library - pass an instance of a class that extends BasePrimitiveLibrary
    # provider - optionally, include a provider (instance of a class that extends BaseProvider)
    def __init__(self, library, provider=None):
        print "Behavior Manager initialized"
        self.test = 0
        self.ig = None  # TODO don't force ppl to refer to the ig directly, give convenience methods in the Manager
        self.library = library
        self.provider = provider
        print("Robot is initialized with library %s and provider %s." % (self.library, self.provider))

    def reset_init(self, library, provider=None):
        self.ig = None
        self.library = library
        self.provider = provider
        print("Robot is reset with library %s and provider %s." % (self.library, self.provider))

    def create_new_ig(self):
        self.ig = IG.IG()

    def save_ig(self, file_name):
        print("Attempting to save %s" % file_name)
        f = open(file_name, "wb")
        pickle.dump(self.ig, f)
        f.close()
        print("Behavior is saved to ", file_name)

    def load_ig(self, fileName):
        f = open(fileName)
        self.ig = pickle.load(f)
        self.ig.reset()
        f.close()
        print("Behavior ",fileName," is loaded")

    def next_node(self):
        if len(self.ig.currentNode.neighbors) > 0:
            self.ig.currentNode = self.ig.currentNode.neighbors[0]
        else:
            self.ig.currentNode = None

    def step(self):
        def check_condition(node):
            if node.useProvider:
                # cond = self.impStore.functionStore[node.Fn](
                cond_result = self.library.get_condition(node.Fn)(
                    self.provider, *node.FnArgs
                )
            else:
                # cond = self.impStore.functionStore[node.Fn](
                cond_result = self.library.get_condition(node.Fn)(
                    *node.FnArgs
                )
                # cond = eval(self.ig.currentNode.codeStr, self.scope)
            return cond_result
        if self.ig.currentNode is not None:
            print("executing step ", self.ig.currentNode.Fn, ' ', self.ig.currentNode.FnArgs)
            print self.ig.currentNode.neighbors
            if self.ig.currentNode.type == InstructionNode.ACTION:
                print("executing action ")
                #exec(self.ig.currentNode.codeStr, self.scope)
                if self.ig.currentNode.useProvider:
                    # self.impStore.functionStore[self.ig.currentNode.Fn](
                    self.library.get_action(self.ig.currentNode.Fn)(
                        self.provider, *self.ig.currentNode.FnArgs
                    )
                else:
                    # self.impStore.functionStore[self.ig.currentNode.Fn](
                    self.library.get_action(self.ig.currentNode.Fn)(
                        *self.ig.currentNode.FnArgs
                    )
                time.sleep(1)
                self.next_node()
            elif self.ig.currentNode.type == InstructionNode.LOOP:
                print "checking loop condition ", self.ig.currentNode.Fn
                cond = check_condition(self.ig.currentNode)
                if cond:
                    print "condition true, continuing the loop"
                    self.next_node()
                else:
                    print "condition false, exiting the loop"
                    if len(self.ig.currentNode.neighbors[1].neighbors) > 1:
                        self.ig.currentNode = self.ig.currentNode.neighbors[1].neighbors[1]
                    else:
                        self.ig.currentNode = None
            elif self.ig.currentNode.type == InstructionNode.CONDITIONAL:
                print "checking if condition"
                #cond = eval(self.ig.currentNode.codeStr, self.scope)
                cond = check_condition(self.ig.currentNode)
                if cond:
                    print "if condition true"
                    self.ig.currentNode = self.ig.currentNode.neighbors[0]
                else:
                    print "if condition false, exiting the loop"
                    self.ig.currentNode = self.ig.currentNode.neighbors[1]

            elif self.ig.currentNode.type == InstructionNode.ENDLOOP:
                print "endloop node"
                self.next_node()
            else:
                print "node type: ", self.ig.currentNode.type
                self.next_node()
            return True
        else:
            print("end of execution")
            return False

    def run(self):
        self.ig.reset()
        while (self.step()):
            pass
