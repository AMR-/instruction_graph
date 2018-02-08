

class InstructionNode:
    START = 0
    STOP = 1
    EMPTY = 2
    ACTION = 3
    CONDITIONAL = 4
    LOOP = 5
    ENDLOOP = 6

    def __init__(self):
        self.type = None
        self.ctype = None # rename, for use with conditionals, ie 'if', 'else', 'endif'
        #self.codeStr = ""
        self.Fn = None
        self.FnArgs = []
        self.useProvider = False
        self.neighbors = []
        self.currentNode = None
        self.start = None
        self.stop = None
        self.stack = []


class IG:
    """An implementation of the Instruction Graphs (Mericli et al., 2013) for robot task specification"""
    def __init__(self):
        self.start = InstructionNode()
        self.start.type = InstructionNode.START
        self.start.codeStr = "start"
        self.stop = InstructionNode()
        self.stop.type = InstructionNode.STOP
        self.stop.codeStr = "stop"
        self.reset()
        # During IG creation, instructionStack holds the
        #   stack of unclosed conditional-type nodes
        self.instructionStack = []
        print("IG initialized")

    def reset(self):
        self.currentNode = self.start
        ## TODO perhaps self.currentNode be define on IG and not InstructionNode?

    def add_action(self, fn_name, parent_node=None, args=None, pass_provider=False):
        if (parent_node is None):
            parent_node = self.currentNode
        #print "adding action ", code
        print("adding action %s with %d arguments and %s provider." % (fn_name,
            len(args) if args is not None else 0,
            'WITH passing a' if pass_provider else 'not passing a'))
        #print "parent; ", parentNode.codeStr
        # print "parent; ", parentNode.Fn, ' ', parentNode.FnArgs
        print("parent; %s %s" % (parent_node.Fn, parent_node.FnArgs))
        n = InstructionNode()
        n.type = InstructionNode.ACTION
        #n.codeStr = code
        n.Fn = fn_name
        n.FnArgs = args if args is not None else []
        n.useProvider = pass_provider
        parent_node.neighbors.append(n)
        self.currentNode = n

    def add_if(self, condition, parent_node = None, args=None, pass_provider=False):
        if (parent_node is None):
            parent_node = self.currentNode
        n = InstructionNode()
        n.type = InstructionNode.CONDITIONAL
        #n.codeStr = condition
        n.Fn = condition
        n.FnArgs = args if args is not None else []
        n.useProvider = pass_provider
        parent_node.neighbors.append(n)
        self.instructionStack.append(n)
        for i in range(3):
            t = InstructionNode()
            t.type = InstructionNode.EMPTY
            n.neighbors.append(t)

        #n.neighbors[0].code = "if"
        #n.neighbors[1].code = "else"
        #n.neighbors[2].code = "endif"
        n.neighbors[0].ctype = "if"
        n.neighbors[1].ctype = "else"
        n.neighbors[2].ctype = "endif"

        self.currentNode = n.neighbors[0]

    def add_else(self):
        ifnode = self.instructionStack[-1]
        self.currentNode.neighbors.append(ifnode.neighbors[2])
        self.currentNode = ifnode.neighbors[1]

    def add_end_if(self):
        ifnode = self.instructionStack.pop()
        self.currentNode.neighbors.append(ifnode.neighbors[2])
        self.currentNode = ifnode.neighbors[2]
        if len(ifnode.neighbors[1].neighbors) == 0:
            ifnode.neighbors[1].neighbors.append(ifnode.neighbors[2])

    def add_loop(self, condition, parent_node=None, args=None, pass_provider=False):
        if (parent_node is None):
            parent_node = self.currentNode
        n = InstructionNode()
        n.type = InstructionNode.LOOP

        n.Fn = condition
        n.FnArgs = args if args is not None else []
        n.useProvider = pass_provider

        parent_node.neighbors.append(n)
        self.currentNode = n
        self.instructionStack.append(n)

    def add_end_loop(self, parent_node = None):
        if (parent_node is None):
            parent_node = self.currentNode
        n = InstructionNode()
        n.type = InstructionNode.ENDLOOP
        #n.codeStr = ""
        n.Fn = ""
        parent_node.neighbors.append(n)
        self.currentNode = n
        beginLoop = self.instructionStack.pop()

        self.currentNode.neighbors.append(beginLoop)
        beginLoop.neighbors.append(self.currentNode)

    def add_stop(self, parent_node=None):
        if (parent_node is None):
            parent_node = self.currentNode

        parent_node.neighbors.append(self.stop)

    def print_nodes(self):
        n = self.start
        while n is not None:
            print(n.type, " ", n.Fn if n.Fn is not None else n.condition, " ", n.neighbors)
            if len(n.neighbors) > 0:
                n = n.neighbors[0]
            else:
                n = None

