from instruction_graph.components.PrimitiveLibrary import BasePrimitiveLibrary
from instruction_graph.components.PrimitiveTuples import ActionPrimitive as Action, ConditionalPrimitive as Cond


# This is an example of a python file you might create to serve as a Primitive Library
class ExamplePrimitiveLibrary(BasePrimitiveLibrary):

    # -- The following three functions implement the required abstract classes from the base class --

    def library_name(self):
        return "Example_Primitive_Library"

    def list_action_primitives(self):
        return [
            Action(fn_name="fun_zero",
                   fn=self.fun_zero,
                   human_name="Function Zero",
                   human_description="This Function is a toy function that returns it's"
                                     "own input and takes no memory object."),
            Action(fn_name='fun_hello', fn=self.fun_hello),  # At minimum, only the function identifying
                                                             #  name and function itself are required
            Action(fn_name='fun_set', fn=self.f_set, human_name='Set Function',
                   human_description='Sets a value in the memory.'),
            Action(fn_name='fun_get', fn=self.f_get, human_name='Get Function',
                   human_description='Gets a value in the memory.'),
            Action(fn_name='fun_3', fn=self.fun_three,
                   human_name='Function 3'),    # can have name and no description
            Action(fn_name='inc', fn=self.f_inc, human_name='Increment Key',
                   human_description='Increment the value found at the specified key by 1.'),
            Action(fn_name='dec', fn=self.f_dec, human_name='Decrement Key',
                   human_description='Decrement the value found at the specified key by 1.'),
            Action("print_args", self.print_args,
                   "Print with Args", "Print the first argument interpolated with the second.")
        ]

    def list_conditional_primitives(self):
        return [
            Cond(fn_name='less', fn=self.con_less, human_name='is less',
                 human_description="Checks if the value of a certain key is less than a given value.  "
                                   "(Returns true if so.)")
        ]

    # -- / end implementation of abstract functions --

    # If no memory object is used, then no need to include an argument for the memory object.  (This is not a
    #   recommended practive.  The default is to pass a memory object.  See print_args and the rest of the
    #   functions in this file.)
    @staticmethod
    def fun_zero(x):
        print(x)

    @staticmethod
    def fun_hello():
        print("Hello")

    # Note that the first argument for a function should be a memory object, if function takes a memory object
    #  (the default).
    # noinspection PyUnusedLocal
    @staticmethod
    def print_args(memory, text, args):
        print(text % args)

    @staticmethod
    def f_set(memory, key, value):
        memory.set(key, value)
        print('%s set to %s' % (key, value))

    @staticmethod
    def f_get(memory, key):
        value = memory.get(key)
        print("%s: %s" % (key, value))

    @staticmethod
    def f_inc(memory, key):
        value = int(memory.get(key)) + 1
        memory.set(key, value)
        print("%s: %s (incremented)" % (key, value))

    @staticmethod
    def f_dec(memory, key):
        value = int(memory.get(key)) - 1
        memory.set(key, value)
        print("%s: %s (decremented)" % (key, value))

    @staticmethod
    def fun_three(memory):
        x = memory.get('x')
        print("x: %d" % x)

    @staticmethod
    def con_less(memory, key, maximum):
        value = int(memory.get(key))
        return value < maximum
