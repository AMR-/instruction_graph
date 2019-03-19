# Transferable Augmented Instruction Graph

Transferable Augmented Instruction Graph (TAIG) is a library that allows the creation of task plans for robots or for other agent-systems.  These task plans can be transferred across systems very easily.

Tasks are created in a graph form with conditionals and loops.  Nodes in the graph refer to "primitives" which are atomic units of work (actions for the system to perform) or conditions to test.

Create an Instruction Graph, and associate it with a Primitive Library and Memory Object (noted below) and you can execute the task on a system.

This paradigm is useful because it allows executing a single task plan across multiple robots/systems.  For a single robot, allows defining atomic functionality once, and re-using it across all the tasks that that robot is to complete.

### Table of Contents
1. [Installation](#Installation)
1. [Introduction](#Introduction)
1. [QuickStart / Example](#QuickStart)
1. [Details for developing your own TAIG](#Details-TAIG)
    1. [Creating Memory](#Memory)
    1. [Creating Primitives](#Primitives)
    1. [Creating the Graph and Saving to File](#GraphSave)
    1. [Running the Graph](#GraphRun)
    1. [Additional Techniques](#Additional)
    1. [Nested Graphs](#Nested)
1. [Interactive Taig](#ITAIG)
1. [Credits](#Credits)

<a name="Installation"></a>
# Installation

To install the library just run

    pip install instruction_graph

instruction_graph has been tested with Python 2.7 and 3.6.

<a name="Introduction"></a>
# Introduction

There are three components to the paradigm:
1. The Memory Object
1. The Primitive Library
1. The Instruction Graph

The Memory Object has fields that store any information required by the application at runtime (session info, database connection, ROS topics, state information, and any other data the application will track and store).

The Primitive Library is an object which holds a collection of Primitives.   A Primitive can be either an Action or a Condition.  Actions are simple actions that are performed.  Conditions are simple conditions that are tested, and can be used in an IF or WHILE node.  Each Primitive has at least a Primitive ID and a function. (See more details below.)

The Instruction Graph is a directed graph.  Each node contains a reference to a primitive.  When the graph is traversed, the function held by the Primitive to which the node refers is executed. (See more details below.)

The Memory Object provides the memory, and should contain no task logic.  The Primitive Library contains Primitives with atomic functionality.  Primitives should be divided into robot/system-specific Primitives and task-specific Primitives (this organizational division is not required, but is just for your own benefit).  Primitives should not have any task logic nor should they refer to system memory directly, but rather use the Memory Object to read/write any data they require.  Primitives should be stateless.   The Instruction Graph contains the task logic.

These three components are modular.  You can switch one out without touching the other two.

During graph creation or execution, we say that a graph is "associated" with a Primitive Library and Memory Object.  This association is performed by Manager.py.

<a name="QuickStart"></a>
## QuickStart / Example

To just quickly run an instruction graph, you can use the example Memory and Library that ships with instruction_graph.

You can run and execute the following code:

```python
from instruction_graph import Manager
from instruction_graph import DefaultMemory, ExamplePrimitiveLibrary

COUNT = "count"
HOW_COOL = "how cool is TAIG?"

A_SET = "fun_set"
A_GET = "fun_get"
A_PRINT = "print_args"
C_LESS = "less"

mem = DefaultMemory()
lib = ExamplePrimitiveLibrary()
m = Manager(memory=mem, library=lib)

m.create_new_ig()
m.ig.add_action(A_SET, args=[COUNT,5])
m.ig.add_action(A_SET, args=[HOW_COOL,"So awesome and cool."])

m.ig.add_if(C_LESS, args=[COUNT, 10])
m.ig.add_action(A_PRINT, args=["The count is less than %d", 10])
m.ig.add_else()
m.ig.add_action(A_PRINT, args=["The count is NOT less than %d", 10])
m.ig.add_end_if()

m.ig.add_action(A_GET, args=[HOW_COOL])
m.save_ig("graph.ig")

m.load_ig("graph.ig")
m.run()
```

You are creating a graph using the example Memory and Primitive Library.  It will set two values in the memory, check one of them in an if condition and print, and then get the value of the other and print it.

This is a basic example, of course, so that you can understand it easily.

<a name="Details-TAIG"></a>
## Details for developing on your own TAIG

Memory, Primitives, and Graph are decoupled and modular.  You can use different Memory Objects with the same or different Graphs, and different Primitive Libraries with the same or different Graphs.   So, you can create them and combine them in any order.

<a name="Memory"></a>
### Creating Memory

Memory is a good place to start as you create your own system.  Technically Memory is not required.  If your application is totally reactive and stateless, then you can just set the memory to None in the Manager.

Probably you will want some memory though.

When creating the memory object, consider all the types of information that you may want to store.  This could be containers for application state information, connections to databases, or anything else you will need.

Create a python file, for example `example_create.py`

Consider this class, similar to DefaultMemory in the QuickStart example:
```python
from instruction_graph.components.Memory import BaseMemory


class DefaultMemory2(BaseMemory):
    def __init__(self):
        super(DefaultMemory2, self).__init__()
        self.info = {}
        self.database_connection = None
        self.counter = 0
        self.whatever = "data"

    def memory_name(self):
        return "Another_Example_Memory"
 ```
It has attributes that an application can use. A Memory object can define any attributes.

Memory Object should extend BaseMemory, and implement the `memory_name` method.

If you want your application to publish to a ROS topic, we recommend adding the rospy.Publisher object as a value to an attribute of the Memory object.   If you want your application to subscribe to a ROS topic, we recommend adding that to the Memory as well, along with any callback (the callback could update additional values in the memory).  Primitives should not subscribe to topics directly, and Primitives should publish to ROS topics by referencing the Publisher on the Memory object.

<a name="Primitives"></a>
### Creating Primitives

Primitives are where the actual low-level functionality for executing task components is stored.

There are two kinds of Primitives, Actions and Conditions.   Actions store atomic functionality, and are meant to be used on Action nodes.  Conditions check conditions, and are meant to be used on IF or WHILE nodes.

Primitive functions can be parameterized (they can take arguments).

To create a primitive, you will first define a function.  A function meant for an action primitive should not have a return value.  A function meant for a condition primtive should return `True` or `False`.

See an example Primitive Library defined below.

```python
from instruction_graph.components.PrimitiveLibrary import BasePrimitiveLibrary
from instruction_graph.components.PrimitiveTuples import ActionPrimitive as Action, ConditionalPrimitive as Cond


class ExamplePrimitiveLibrary2(BasePrimitiveLibrary):
    def library_name(self):
        return "Example_Primitive_Library_2"

    def list_action_primitives(self):
        return [
            Action(fn_name='set', fn=self.set_value, human_name='Set Function', human_description='Sets a value in the memory.'),
            Action("print_args", self.print_args, "Print with Args", "Print the first argument interpolated with the second."),
            Action("dec", self.decrement, "Decrement Key", "Decrement the value found at the specified key by 1")
        ]

    def list_conditional_primitives(self):
        return [
            Cond('less', self.check_if_less, human_name='is less', human_description="Checks if the value of a certain key is less than a given value. (Returns true if so.)")
        ]

    # Actions #

    @staticmethod
    def print_args(memory, text, args):
        print(text % args)

    @staticmethod
    def set_value(memory, key, value):
        memory.info[key] = value
        print('%s set to %s' % (key, value))

    @staticmethod
    def decrement(memory, key):
        value = memory.info[key] - 1
        memory.info[key] = value
        print("%s: %s (decremented)" % (key, value))

    # Conditions #

    @staticmethod
    def check_if_less(memory, key, maximum):
        value = int(memory.info[key])
        return value < maximum
```

Note how functions are defined and then referenced in the ActionPrimitive and ConditionPrimitive instantiations.

Required methods are:
* library_name - a string to indicate this library's name, used in logging
* list_action_primitives - should return a list of ActionPrimitives
* list_conditional_primitives - should return a list of ConditionalPrimitives

<a name="GraphSave"></a>
### Creating the Graph and Saving to File

Let's use our Memory and PrimitiveLibrary from above in creating an instruction graph.

We instantiate a Manager object, specifying the Memory and PrimitiveLibrary objects that we created above.

This particular graph will set the value of "count" in the memory to 6.

Then it will kick off a loop that will run until "count" is less than 1.  In each iteration of the loop it will check if "count" is less than 3.  If so, it will print "count is less than 3" and if not it will print "count is greater than or equal to 3".  Then "count" will be decremented.

Finally, the graph will be saved to "graph_filename.ig"

```python
from instruction_graph import Manager

mem_obj = DefaultMemory2()
eg_library = ExamplePrimitiveLibrary2()
igm = Manager(library=eg_library, memory=mem_obj)
ct = "count"
igm.create_new_ig()
igm.ig.add_action("set", args=[ct, 6])
igm.ig.add_loop('less', args=[ct, 1], negation=True)

igm.ig.add_if('less', args=[ct, 3])
igm.ig.add_action("print_args", args=["count is less than %d", 3])
igm.ig.add_else()
igm.ig.add_action("print_args", args=["count is greater than or equal to %d", 3])
igm.ig.add_end_if()

igm.ig.add_action("dec", args=[ct])
igm.ig.add_end_loop()
igm.save_ig("graph_filename.ig")
```

Run this code to check it out!

<a name="GraphRun"></a>
### Running the Graph

After you have created "graph_filename.ig," you can load it and run it.

Use the following code to do so (you can reuse the existing Manager or create a new one as show).
This can be in the same file, or in a new file called `example_run.py`
```python
from instruction_graph import Manager
from example_create import DefaultMemory2,ExamplePrimitiveLibrary2


mem_obj = DefaultMemory2()
eg_library = ExamplePrimitiveLibrary2()
igm = Manager(library=eg_library, memory=mem_obj)

igm.load_ig("graph_filename.ig")
igm.run()
```

Note that the graph can be run on a system right from the file.  You do not need to create anew.  Make sure that the Primitive Library and Memory Object you use with a graph are compatible.

<a name="Additional"></a>
### Additional Techniques

There is a special type of node you can add to a graph called a 'halt condition'.  Whenever the halt condition becomes true, the graph execution immediately stops.  To add a halt condition, use the *set_halt_condition* command. Add a line according to the following example anytime during graph creation:

```python
igm.ig.set_halt_condition("less_or_no_key", args=["key1", 7], negation=True)
```

In this case, the example primitive used with the arguments shown in the example line mean that the graph execution would halt if _key1_ was defined and if its value exceeded 7.  Like other conditional primitives, this can be negated or not, and used with whatever arguments you desire.

This is useful if you are on a robot system with an emergency stop button, or if you want your agent to terminate execution immediately under other scenarios.

<a name="Nested"></a>
### Nested Graphs (Graphs as Primitives)

You can use the special built in "run_ig" action primitive to include a node that attempts to run a different graph.  In this manner, graphs can be nested within other graphs.  The manager will attempt to look for the graph in the same directory to which all graphs are being saved (so if you are going to used previously saved graphs, ensure these directories are the same).

When running a sub-graph, the entire graph executes before the node on the upper graph is exited.  The library and memory in the parent graph and passed to the child during execution, and updates to the memory object made by the child graph execution will persist when execution continues on the parent graph.  There is no limit to how much you can nest graphs (aside from the practical consideration of computer memory).

The default name of the primitive to run a graph is "run_ig".  If this is the name of another primitive in the user-defined library, a different name is chosen.  If the library subclasses BasePrimitiveLibrary as described in this documentation, then the name of the primitive will be stored in the **run_ig_name** attribute of the library, and can be retrieved therefrom.

There are two ways to run a graph: explicitly by name and by checking the queued name. (The latter allows for dynamic selection of graph to run.)

To run a sub-graph explicitly, consider the following line:
```python
igm.ig.add_action(igm.library.run_ig_name, args=[path_to_graph_as_string])
```
This will put a node in the graph that contains the instruction to run the graph _path_to_graph_as_string_ when it is executed.

Please do note that it is the instruction that is added to the graph and not the child graph itself.  If the subgraph changes (if a new file is saved to the same filename), it is this new graph that will be loaded and executed at runtime.

To run a sub-graph dynamically, find the structure to do so in the following two lines:
```python
igm.ig.add_action("queue_ig", args=[path_to_graph_as_string])
igm.ig.add_action(igm.library.run_ig_name)
```
A path to the graph to run is queued up with the "queue_ig" primitive. Then, _run_ig_ is run without arguments to indicate accessing it this variable .

The "queue_ig" method is not included by default, but it is in the example primitive library where it is defined as follows:
```python
    @staticmethod
    def queue_ig_prim(memory, path):
        memory.queue_ig_as_primitive(path)
```
You can copy this implementation or write your own to achieve this functionality.  If you use a Memory that extends BaseMemory, then the **queue_ig_as_primitive** and **get_queued_ig** methods will be inherited by the memory and can be referenced in the above manner.

If a halt condition is included on a graph used as a child graph, and the halt condition becomes satisfied, child graph execution will terminate, and execution of the parent graph will continue on to the next node.  This has two ramifications:
1. The parent graph does not know if the child graph completed successfully
1. Sub-tasks can be terminated without stopping agent execution

<a name="ITAIG"></a>
# Interactive TAIG

For documentation on Interactive TAIG, please go [here](documentation/InteractiveManager.md)

<a name="Credits"></a>
# Credits

The Instruction Graph Library has been created by
* Aaron M. Roth
* Çetin Meriçli
* Steven D. Klee