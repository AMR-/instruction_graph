# Interactive Manager

The Interactive Manager (IM) extends the Manager and acts as an agent.  You, another human, or another computer system can then interact with the IM over a text-based interface to execute primitives, create task graphs, and executive task graphs.

There are a few steps towards using the IM.

First, define Primitives with appropriate elements.  Then instantiate the IM and use it.

When the IM is evaluating an input, it attempts to make sense of the request, and then handle it.

## Primitive Library for IM

Defining a Primitive Library for use with an IM is similar to defining it for use normally.  Primitive functions are implemented the same.  The only difference is that when creating *ActionPrimitive* and *ConditionPrimitive* objects and listing them in the **list_action_primitives** and **list_conditional_primitives** functions, additional properties are added.

See an example Primitive Library defined below.

```python
from instruction_graph.components.PrimitiveLibrary import BasePrimitiveLibrary
from instruction_graph.components.PrimitiveTuples import ActionPrimitive as Action, ConditionalPrimitive as Cond


class ExamplePrimitiveLibrary2(BasePrimitiveLibrary):
    def library_name(self):
        return "Example_Primitive_Library_2"

    def list_action_primitives(self):
        return [
            Action(fn_name='im_set', fn=self.f_set, human_name='Set Function',
                   human_description='Sets a value in the memory.',
                   match_re_or_fn="set [a-z0-9 ]+ to [a-z0-9 ]+", argparse_re_or_fn="set (.*) to (.*)",
                   parsed_description=lambda args: "Set the value of '%s' to '%s'" % (args[0], args[1])),
            Action(fn_name='im_inc', fn=self.increment, human_name='Increment Key',
                   human_description='Increment the value found at the specified key by 1.',
                   match_re_or_fn="inc(rement)? [a-z0-9 ]+", argparse_re_or_fn="inc(?:rement)? ([a-z0-9 ]+)"),
            Action(fn_name='im_dec', fn=self.decrement, human_name='Decrement Key',
                   human_description='Decrement the value found at the specified key by 1.',
                   match_re_or_fn="dec(rement)? [a-z0-9 ]+", argparse_re_or_fn="dec(?:rement)? ([a-z0-9 ]+)",
                   parsed_description=lambda args: "Decrement %s by one" % args[0]),
        ]

    def list_conditional_primitives(self):
        return [
            Cond(fn_name='less', fn=self.check_if_less, human_name='is less',
                 human_description="Checks if the value of a certain key is less than a given value.  "
                                   "(Returns true if so.)",
                 match_re_or_fn="[a-z0-9 ]+ is less than [0-9]+",
                 argparse_re_or_fn="([a-z0-9 ]+) is less than ([0-9]+)",
                 parsed_description=lambda args: "The value of '%s' is less than %s" % (args[0], args[1])),
        ]

    # Actions #

    @staticmethod
    def f_set(memory, key, value):
        memory.set(key, value)
        print('%s set to %s' % (key, value))

    @staticmethod
    def increment(memory, key):
        value = int(memory.get(key)) + 1
        memory.set(key, value)
        print("%s: %s (incremented)" % (key, value))

    @staticmethod
    def decrement(memory, key):
        value = int(memory.get(key)) - 1
        memory.set(key, value)
        print("%s: %s (decremented)" % (key, value))

    # Conditions #

    @staticmethod
    def check_if_less(memory, key, maximum):
        value = int(memory.info[key])
        return value < maximum
```

This is very similar to the example Primitive Library noted before, with additional Primitive attributes as follows:
* **match_re_or_fn**: This is a regular expression or function (returning a boolean). When the IM receives text input, it uses this parameter to determine if this is a primitive to which the text is referring. If the regex matches, or the function returns true, it is considered a match.
* **argparse_re_or_fn**: This is a regular expression or function (returning a list of strings). After a piece of input text has been identified as referring to a primitive, this function is called to determine how to parameterize it.  If it is a regular expression, each capturing group is a parameter. If **argparse_re_or_fn** is ommitted, no parameters are passed to the primitive.
* **parsed_description**: This is a function that takes in a list of arguments and returns a string.  It is used by the agent to respond to the user, for describing a parameterized primitive. If **parsed_description** is not specified, the **human_description** is used.

Note that primitives you create for use in the interactive manager might receive their arguments as strings.  You should ensure that the functions defined for the primitives themselves do any type conversion required.

## Using the Interactive Manager

Find an example of instantiating the Interactive Manager with example Memory and Primitive Library below.

```python
from instruction_graph.interactive.InteractiveManager import InteractiveManager
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary

memory_obj = DefaultMemory()
library = ExamplePrimitiveLibrary()
im = InteractiveManager(library=library, memory=memory_obj)

resp = im.parse_input_text("set key 1 to 3")
print(resp)
resp = im.parse_input_text("I will teach you to dance")
print(resp)
...
resp = im.parse_input_text("Done Learning")
print(resp)
```

The IM is initialized with a library and a memory.  It creates a Manager inside itself which it uses to build a graph if necessary.

The **parse_input_text** method takes in text.  The IM agent will perform any actions and return its response as a string.  Actions may involve executing primitives/graphs or building/saving graphs.

The IM can exist in four states:
* WAITING: can be commanded to execute a primitive, execute a graph, or start learning a new graph
* CONFIRM_LEARN_IG: after being asked to start a new graph, the IM will ask for confirmation
* LEARNING_IG_WAITING: During construction of a new graph, can be instructed to add a primitive to the graph, or stop learning the graph
* CONFIRM_ADD_PRIM_WHEN_LEARNING: when the IM believes it has heard a primitive to add to the graph, it will repeat what it has heard and ask for confirmation.
The state is stored on the state attribute (_im.state_) in above. It should never be necessary to access, it is described here merely of interest and as it may help you understand what is going on.

The manner in which a primitive is recognized is the same for executing or adding.  **match_re_or_fn** is used to match, **argparse_re_or_fn** is used to parse primitives, and **parsed_description** is used during the confirmation request. Matching attempts are processed in the order in which they are listed in the return from **list_conditional_primitives** or **list_action_primitives**.

One primitive is added to the graph at a time.

The grammar for the communication itself is noted by the Builder Phrases, noted in the next section.

For additional technical description on the IM, read the thesis noted on the Credits section on the top-level Readme (or just check out the code).

## Builder Phrases

Please see the following table of Builder Phrases, which entail the commands or requests that the IM will understand.  The first column shows the attribute name in the BuilderPhrases object, the second column shows the (configurable, default) value, and the third column has a description of the purpose and meaning.  In the table, the non-IM agent is referred to as a human for clarity, although as mentioned, it doesn't have to be a human, it could be another computer agent.


Attribute | Default | Description
--- | --- | ---
teach_you | `regex("i will teach you to (.*)")` | human instruction to IM to begin learning a graph with name in the first captured group
confirm_pos | `regex("y(?:es\|eah)?")` | human affirmative
confirm_neg | `regex("no")` | human negative
teaching_done | `regex("done (?:learning\|teaching)")` | human instruction to IM to save and finish graph currently under construction
h_if_cond | `regex("if (?P<neg>(?:not\|don'?t) )?(?P<cmd>.*)")` | add a conditional primitive specified by the <cmd> capturing group as an IF condition to the graph.  If the <neg> capturing group is present, negate it.
h_while_cond | `regex("(?:while\|loop) (?P<neg>(?:not\|don'?t) )?(?P<cmd>.*)")` | add a conditional primitive specified by the <cmd> capturing group as a WHILE/LOOP condition to the graph.  If the <neg> capturing group is present, negate it.
h_else | `regex("else")` | add an ELSE node
h_end_if | `regex("end if")` | add an END IF node
h_end_loop | `regex("end loop")` | add an END LOOP node
run_ig | `regex("run (.*)")` | if in state WAITING, execute the saved graph specified by the capturing group. if in the process of building a graph, add a *run_ig* node to run a graph with this name
agent_start | `"Beginning interactive graph runner and builder."` | IM outputs this at startup
exec_prim_success | `""` | when a primitive is successfully *executed*, the IM responds with this
exec_prim_fail | `"Could not find or run primtive <prim_id>"` | What to output when the IM believes the human specified a primitive but it can't find the primitive specified
exec_graph_success | `""` | the IM outputs this after successfully executing a graph
exec_graph_fail | `"Could not find or run graph <prim_id>"` | What to output when the IM believes the human specified a graph but it can't find the graphspecified in the directory
build_new_graph | `"I will learn to <name>?"` | when the IM believes that the human has asked it to learn a new graph, it outputs a request for confirmation
yes_learn | `"Ok, I am ready to learn.  What is first?"` | The IM outputs this at the beginning of learning a graph.
no_learn | `"Ok"` | The IM outputs this after receiving a negative response to checking whether it should learn a graph
unclear_confirm | `"I don't understand. Please name a primitive to add or tell me I'm done."` | The IM outputs this when it cannot process the human response after the IM asks for a yes/no response.
unclear_learn | `"I don't understand. Please name a primitive to add or tell me I'm done."` | The IM outputs this if it doesn't understand text input during graph construction.
confirm_new_primitive | `"I should <cond> <name>"` | During graph construction, the IM asks for confirmation for adding a primitive using this construction. *<name>* will be replaced with the name of the primitive (including parameters), and <cond> will be replaced by any of the following if required: IF, WHILE, NOT
new_primitive_confirmed_pos | `"Ok, what's next?"` | When the human responds confirming adding a node, the IM outputs this.
new_primitive_confirmed_neg | `"Ok, what's next?"` | When the human responds rejecting confirmation of adding a node, the IM outputs this.
confirm_add_run_graph_name | `"run the graph <name>"` | The IM uses this construction to confirm adding a *run_ig* node
new_run_graph_not_exist | `"The graph you are requesting I add does not seem to exist. I checked for it at <location>."` | when attempting to add a *run_ig* node to a graph, this is output if the graph is not fond
done_building_graph | `"I have learned <name>."` | When the IM saves a graph and exits graph construction, it outputs this.

Any text input not matching a phrase from Builder Phrases is assumed to refer to an action primitive that should be executed or added.

You can customize your own BuilderPhrases and use those with the Interactive Manager, as shown below.

```python
from instruction_graph.interactive.InteractiveManager import InteractiveManager, BuilderPhrases
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary
from instruction_graph.interactive.utils import regex

memory_obj = DefaultMemory()
library = ExamplePrimitiveLibrary()

builder_phrases = BuilderPhrases()
builder_phrases.confirm_pos = regex("(Yes|Yeah|Righto)")
builder_phrases.confirm_neg = regex("Nope")
builder_phrases.agent_start = "Get ready! It's interactive time."

im = InteractiveManager(library=library, memory=memory_obj, phrases=builder_phrases)
```
