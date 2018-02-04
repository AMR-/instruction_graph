import pickle
import time

import IG
from IG import InstructionNode
from imp_store.ImplementationStore import ImplementationStore as IStore


class Manager:
    def __init__(self):
        print "Behavior Manager initialized"
        self.test = 0
        self.ig = None
        #self.scope = {}
        self.impStore = None
        self.provider = None

    # add fn_list for raw dictionary of "name" to function def
    #   optionally, include the provider
    #   optionally, name this implementation store
    #   also optionally, pass an already instantiated implementation store
    #   if a full imp store is passed, it is used instead of fn_list
    def init_robot(self, fn_list=None, name=None, provider=None, imp_store=None):
        if imp_store is not None:
            self.impStore = imp_store
        elif imp_store is None and fn_list is not None:
            self.impStore = IStore(name)
            self.impStore.set_fn_store(fn_list)
        else:
            raise ValueError("Must specify either fn_list or imp_store")
        if provider:
            self.provider = provider
        print("Robot is initialized with implementation store %s." % self.impStore.name)

    def createNewIG(self):
        self.ig = IG.IG()

    def saveImpStore(self, fileName=None):
        fileName = fileName if fileName is not None else self.impStore.name
        f = open(fileName,"wb")
        pickle.dump(self.impStore,f)
        f.close()
        print("Implementation Specific Behavior Options saved to ", fileName)

    def loadImpStore(self, fileName):
        f = open(fileName)
        self.impStore = pickle.load(f)
        f.close()
        print("Implementation Specific Behavior Options ",fileName," is loaded")

    def saveIG(self, fileName):
        print("Attempting to save %s" % fileName)
        f = open(fileName, "wb")
        pickle.dump(self.ig, f)
        f.close()
        print("Behavior is saved to ", fileName)

    def loadIG(self, fileName):
        f = open(fileName)
        self.ig = pickle.load(f)
        self.ig.reset()
        f.close()
        print("Behavior ",fileName," is loaded")

    def nextNode(self):
        if len(self.ig.currentNode.neighbors) > 0:
            self.ig.currentNode = self.ig.currentNode.neighbors[0]
        else:
            self.ig.currentNode = None

    def step(self):
        def check_condition(node):
            if node.useProvider:
                cond = self.impStore.functionStore[node.Fn](
                    self.provider, *node.FnArgs
                )
            else:
                cond = self.impStore.functionStore[node.Fn](
                    *node.FnArgs
                )
                #cond = eval(self.ig.currentNode.codeStr, self.scope)
            return cond
        if self.ig.currentNode is not None:
            print("executing step ", self.ig.currentNode.Fn, ' ', self.ig.currentNode.FnArgs)
            print self.ig.currentNode.neighbors
            if self.ig.currentNode.type == InstructionNode.ACTION:
                print("executing action ")
                #exec(self.ig.currentNode.codeStr, self.scope)
                if self.ig.currentNode.useProvider:
                    self.impStore.functionStore[self.ig.currentNode.Fn](
                        self.provider, *self.ig.currentNode.FnArgs
                    )
                else:
                    self.impStore.functionStore[self.ig.currentNode.Fn](
                        *self.ig.currentNode.FnArgs
                    )
                time.sleep(1)
                self.nextNode()
            elif self.ig.currentNode.type == InstructionNode.LOOP:
                print "checking loop condition ", self.ig.currentNode.Fn
                cond = check_condition(self.ig.currentNode)
                if cond:
                    print "condition true, continuing the loop"
                    self.nextNode()
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
                self.nextNode()
            else:
                print "node type: ", self.ig.currentNode.type
                self.nextNode()
            return True
        else:
            print("end of execution")
            return False

    def run(self):
        self.ig.reset()
        while (self.step()):
            pass
