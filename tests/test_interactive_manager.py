import os
# import unittest as ut
from test_base import TestBase

from instruction_graph.interactive.InteractiveManager import InteractiveManager, States
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestInteractiveManager(TestBase):
    @classmethod
    def skip(cls):
        return False

    memory_obj = None
    task_name = "count special"

    # noinspection PyPep8Naming,Reason-overridden method
    def setUp(self):
        TestInteractiveManager.memory_obj = DefaultMemory()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit,Reason-ut
        self.m = InteractiveManager(library=library, memory=TestInteractiveManager.memory_obj)

    def test_im_run_action_primitive(self):
        self.assertEquals(self.m.state, States.WAITING)

        resp = self.m.parse_input_text("set key 1 to 3")
        self.assertEquals(resp, "Executed Set the value of 'key 1' to '3'")
        self.assertEquals(self.m.state, States.WAITING)
        self.assertEquals(self.memory_obj.get("key 1"), "3")

        resp = self.m.parse_input_text("inc key 1")
        self.assertEquals(resp, "")
        self.assertEquals(self.m.state, States.WAITING)
        self.assertEquals(self.memory_obj.get("key 1"), 4)

        resp = self.m.parse_input_text("garble waggle")
        self.assertEquals(resp, "Could not find or run primitive garble waggle")
        self.assertEquals(self.m.state, States.WAITING)

    def test_im_dont_learn_a_graph(self):
        self.assertEquals(self.m.state, States.WAITING)

        resp = self.m.parse_input_text("I will teach you to dance heartily")
        self.assertEquals(resp, "I will learn to dance heartily?")
        self.assertEquals(self.m.state, States.CONFIRM_LEARN_IG)

        resp = self.m.parse_input_text("Bleh")
        self.assertEquals(resp, "I don't understand. Can you please confirm 'yes' or 'no' please?")
        self.assertEquals(self.m.state, States.CONFIRM_LEARN_IG)

        resp = self.m.parse_input_text("No")
        self.assertEquals(resp, "Ok")
        self.assertEquals(self.m.state, States.WAITING)

    # The graph that it learns, named "count special":
    #   set key 1 = val 56
    #   set key 2 = 4
    #   set key 3 = 4
    #   set key 4 = 0
    #   set key 5 = 0
    #   while key 2 < 10
    #       inc key 2
    #       inc key 3
    #       if key 2 < 7
    #           inc key 4
    #       else
    #           inc key 5
    #       end
    #   end loop
    #   while not key 3 < 6
    #       dec key 3
    #   end loop
    def test_im_learn_a_graph(self):
        self.assertEquals(self.m.state, States.WAITING)
        self.assertEquals(self.m.startup_greeting(), "Beginning interactive graph runner and builder.")

        resp = self.m.parse_input_text("I will teach you to %s" % self.task_name)
        self.assertEquals(resp, "I will learn to %s?" % self.task_name)
        self.assertEquals(self.m.state, States.CONFIRM_LEARN_IG)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, I am ready to learn.  What is first?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 1 to 56")
        self.assertEquals(resp, "I should  Set the value of 'key 1' to '56'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("no")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 1 to 56")
        self.assertEquals(resp, "I should  Set the value of 'key 1' to '56'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("blarg")
        self.assertEquals(resp, "I don't understand. Can you please confirm 'yes' or 'no' please?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 2 to 4")
        self.assertEquals(resp, "I should  Set the value of 'key 2' to '4'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 3 to 4")
        self.assertEquals(resp, "I should  Set the value of 'key 3' to '4'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("garble garble key 3")
        self.assertEquals(resp, "I don't understand. Please name a primitive to add or tell me I'm done.")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 4 to 0")
        self.assertEquals(resp, "I should  Set the value of 'key 4' to '0'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("set key 5 to 0")
        self.assertEquals(resp, "I should  Set the value of 'key 5' to '0'?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("while key 2 is less than 10")
        self.assertEquals(resp, "I should  start a while loop with condition  The value of 'key 2' is less than 10?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("increment key 2")
        self.assertEquals(resp, "I should  Increment Key?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("inc key 3")
        self.assertEquals(resp, "I should  Increment Key?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("if key 2 is less than 7")
        self.assertEquals(resp, "I should  start an if condition with condition  "
                                "The value of 'key 2' is less than 7?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("inc key 4")
        self.assertEquals(resp, "I should  Increment Key?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("else")
        self.assertEquals(resp, "I should  add an else clause to the if condition?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("no")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("else")
        self.assertEquals(resp, "I should  add an else clause to the if condition?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("inc key 5")
        self.assertEquals(resp, "I should  Increment Key?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("end if")
        self.assertEquals(resp, "I should  end the if condition?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("end loop")
        self.assertEquals(resp, "I should  end the loop?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("while not key 3 is less than 6")
        self.assertEquals(resp, "I should  start a while loop with negated condition  "
                                "The value of 'key 3' is less than 6?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("dec key 3")
        self.assertEquals(resp, "I should  Decrement key 3 by one?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)

        resp = self.m.parse_input_text("end loop")
        self.assertEquals(resp, "I should  end the loop?")
        self.assertEquals(self.m.state, States.CONFIRM_ADD_PRIM_WHEN_LEARNING)

        resp = self.m.parse_input_text("yes")
        self.assertEquals(resp, "Ok, what's next?")
        self.assertEquals(self.m.state, States.LEARNING_IG_WAITING)
        resp = self.m.parse_input_text("done learning")
        self.assertEquals(resp, "I have learned count special.")
        self.assertEquals(self.m.state, States.WAITING)
        self.assertIn(self.task_name.replace(' ', '_') + '.ig', os.listdir(self.out_folder))

    def test_im_run_graph_made(self):
        self.assertEquals(self.m.state, States.WAITING)

        resp = self.m.parse_input_text("run non-existant graph")
        self.assertEquals(resp, "Could not find or run graph generated/non-existant_graph.ig")
        self.assertEquals(self.m.state, States.WAITING)

        resp = self.m.parse_input_text("run count special")
        self.assertEquals(resp, "")
        self.assertEquals(self.m.state, States.WAITING)
        self.assertEquals(self.memory_obj.get("key 1"), "56")
        self.assertEquals(self.memory_obj.get("key 2"), 10)
        self.assertEquals(self.memory_obj.get("key 3"), 5)
        self.assertEquals(self.memory_obj.get("key 4"), 2)
        self.assertEquals(self.memory_obj.get("key 5"), 4)

    # TODO add test for instructing running a graph inside a graph
