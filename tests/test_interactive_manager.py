import os
# import unittest as ut
from test_base import TestBase

from instruction_graph.interactive.InteractiveManager import InteractiveManager, States
from instruction_graph.example.DefaultMemory import DefaultMemory
from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestInteractiveManager(TestBase):
    memory_obj = None

    def setUp(self):
        # raise ut.SkipTest("DEBUG")
        TestInteractiveManager.memory_obj = DefaultMemory()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit
        self.m = InteractiveManager(library=library, memory=TestInteractiveManager.memory_obj)

    def test_im_run_action_primitive(self):
        # TODO test two primitives
        # TODO test response to unknown
        pass

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

    def test_im_learn_a_graph(self):
        self.assertEquals(self.m.state, States.WAITING)
        self.assertEquals(self.m.startup_greeting(), "Beginning interactive graph runner and builder.")
        # TODO - massive -- run through whole sequence of possibilities in this test
        pass
        # self.assertEquals(TestRunIG.memory_obj.get("key1"), "val1")
        # self.assertIn(ig1_name, os.listdir(TestRunIG.out_folder))

    def test_im_run_graph_made(self):
        # TODO
        pass
