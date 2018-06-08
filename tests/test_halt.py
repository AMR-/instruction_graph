import os
import unittest as ut
from test_base import TestBase

from instruction_graph.core.Manager import Manager
from instruction_graph.example.DefaultMemory import DefaultMemory

from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestHalt(TestBase):

    @classmethod
    def skip(cls):
        return False

    memory_obj = None
    igs = {}

    halt_ig = "ig_halt.ig"
    halt_ig2 = "ig_halt2.ig"
    loop_ig = "ig_loop_halt.ig"
    halt_parent_ig = "ig_halt_parent.ig"

    def setUp(self):
        TestHalt.memory_obj = DefaultMemory()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit
        self.igm = Manager(library=library, memory=TestHalt.memory_obj)

    def test_create_and_save_simple_halt_IG(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action("print_args", args=["yay", ()])
        self.igm.ig.add_action("fun_set", args=["key1", 1])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.add_action("inc", args=["key1"])
        self.igm.ig.set_halt_condition("less_or_no_key", args=["key1", 3], negation=True)
        ig1_name = TestHalt.halt_ig
        ig1_path = TestHalt.out_folder + ig1_name
        TestHalt.igs[TestHalt.halt_ig] = ig1_path
        self.igm.save_ig(ig1_path)
        self.assertIn(ig1_name, os.listdir(TestHalt.out_folder))

    def test_load_and_run_simple_halt_IG(self):
        self.igm.load_ig(TestHalt.igs[TestHalt.halt_ig])
        self.igm.run()
        self.assertEquals(TestHalt.memory_obj.get("key1"), 3)

    def test_create_and_save_simple_halt_IG2_and_halt_parent(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action("print_args", args=["yay", ()])
        self.igm.ig.add_action("fun_set", args=["key1", 4])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.set_halt_condition("less", args=["key1", 3])
        ig2_name = TestHalt.halt_ig2
        ig2_path = TestHalt.out_folder + ig2_name
        TestHalt.igs[TestHalt.halt_ig2] = ig2_path
        self.igm.save_ig(ig2_path)
        self.assertIn(ig2_name, os.listdir(TestHalt.out_folder))

        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=["key2", "begin"])
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig2_path])
        self.igm.ig.add_action("dec", args=["key1"])
        self.igm.ig.add_action("fun_set", args=["key3", "end ok"])
        ig3_name = TestHalt.halt_parent_ig
        ig3_path = TestHalt.out_folder + ig3_name
        TestHalt.igs[TestHalt.halt_parent_ig] = ig3_path
        self.igm.save_ig(ig3_path)
        self.assertIn(ig3_name, os.listdir(TestHalt.out_folder))

    def test_load_and_run_simple_halt_IG2(self):
        self.igm.load_ig(TestHalt.igs[TestHalt.halt_ig2])
        self.igm.run()
        self.assertEquals(TestHalt.memory_obj.get("key1"), 2)

    def test_load_and_run_halt_parent(self):
        self.igm.load_ig(TestHalt.igs[TestHalt.halt_parent_ig])
        self.igm.run()
        self.assertEquals(TestHalt.memory_obj.get("key2"), "begin")
        self.assertEquals(TestHalt.memory_obj.get("key1"), 1)
        self.assertEquals(TestHalt.memory_obj.get("key3"), "end ok")

    def test_create_and_save_cond_loop_halt_IG(self):
        ct = "count"
        self.igm.create_new_ig()
        self.igm.ig.set_halt_condition("less_or_no_key", args=[ct, 3], negation=True)
        self.igm.ig.add_action("fun_set", args=[ct, -2])
        self.igm.ig.add_loop('less', args=[ct, 8])
        self.igm.ig.add_action("inc", args=[ct])
        self.igm.ig.add_end_loop()
        ig2_path = TestHalt.out_folder + TestHalt.loop_ig
        TestHalt.igs[TestHalt.loop_ig] = ig2_path
        self.igm.save_ig(ig2_path)
        self.assertIn(TestHalt.loop_ig, os.listdir(TestHalt.out_folder))

    def test_load_and_run_cond_loop_halt_IG(self):
        self.igm.load_ig(TestHalt.igs[TestHalt.loop_ig])
        self.igm.run()
        self.assertEquals(TestHalt.memory_obj.get("count"), 3)


def main():
    ut.main()


if __name__ == "__main__":
    main()
