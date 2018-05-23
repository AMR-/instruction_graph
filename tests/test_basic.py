import os
import unittest as ut
from test_base import TestBase

from instruction_graph.core.Manager import Manager
from instruction_graph.example.DefaultMemory import DefaultMemory

from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestBasic(TestBase):

    memory_obj = None
    igs = {}

    simple_ig = "ig1.ig"
    loop_ig = "ig2.ig"
    loop_neg_ig = "ig4.ig"
    conditional_ig = "ig3.ig"

    def setUp(self):
        TestBasic.memory_obj = DefaultMemory()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit
        self.igm = Manager(library=library, memory=TestBasic.memory_obj)

    def test_create_and_save_simple_IG(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_zero", args=["Action 1"], pass_memory_obj=False)
        self.igm.ig.add_action("fun_hello", pass_memory_obj=False)
        self.igm.ig.add_action("fun_zero", args=["Action 3"], pass_memory_obj=False)
        self.igm.ig.add_action("fun_hello", pass_memory_obj=False)
        self.igm.ig.add_action("fun_set", args=["key1", "val1"], pass_memory_obj=True)
        ig1_name = TestBasic.simple_ig
        ig1_path = TestBasic.out_folder + ig1_name
        TestBasic.igs[TestBasic.simple_ig] = ig1_path
        self.igm.save_ig(ig1_path)
        self.assertIn(ig1_name, os.listdir(TestBasic.out_folder))

    def test_load_and_run_simple_IG(self):
        self.igm.load_ig(TestBasic.igs[TestBasic.simple_ig])
        self.igm.run()
        self.assertEquals(TestBasic.memory_obj.get("key1"), "val1")

    def test_create_and_save_cond_loop_IG(self):
        ct = "count"
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=[ct, 0])
        self.igm.ig.add_loop('less', args=[ct, 4])
        self.igm.ig.add_action("inc", args=[ct])
        self.igm.ig.add_end_loop()
        ig2_path = TestBasic.out_folder + TestBasic.loop_ig
        TestBasic.igs[TestBasic.loop_ig] = ig2_path
        self.igm.save_ig(ig2_path)
        self.assertIn(TestBasic.loop_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_loop_IG(self):
        self.igm.load_ig(TestBasic.igs[TestBasic.loop_ig])
        self.igm.run()
        self.assertEqual(TestBasic.memory_obj.get("count"), 4)

    def test_create_and_save_cond_loop_IG_with_negation(self):
        ct = "count"
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=[ct, 6])
        self.igm.ig.add_loop('less', args=[ct, 4], negation=True)
        self.igm.ig.add_action("dec", args=[ct])
        self.igm.ig.add_end_loop()
        ig4_path = TestBasic.out_folder + TestBasic.loop_neg_ig
        TestBasic.igs[TestBasic.loop_neg_ig] = ig4_path
        self.igm.save_ig(ig4_path)
        self.assertIn(TestBasic.loop_neg_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_loop_IG_with_negation(self):
        self.igm.load_ig(TestBasic.igs[TestBasic.loop_neg_ig])
        self.igm.run()
        self.assertEqual(TestBasic.memory_obj.get("count"), 3)

    def test_create_and_save_cond_if_IG(self):
        ct = "count1"
        ct2 = "count2"
        ct3 = "count3"
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=[ct, 0])
        self.igm.ig.add_action("fun_set", args=[ct2, 10])
        self.igm.ig.add_action("fun_set", args=[ct3, 10])

        self.igm.ig.add_if('less', args=[ct, 4])
        self.igm.ig.add_action("fun_set", args=[ct, "Yes"])
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct, "No"])
        self.igm.ig.add_end_if()

        self.igm.ig.add_if('less', args=[ct2, 4], negation=False)
        self.igm.ig.add_action("fun_set", args=[ct2, "Yes"])
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct2, "No"])
        self.igm.ig.add_end_if()

        self.igm.ig.add_if('less', args=[ct3, 4], negation=True)
        self.igm.ig.add_action("fun_set", args=[ct3, "Yes"])
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct3, "No"])
        self.igm.ig.add_end_if()

        ig3_path = TestBasic.out_folder + TestBasic.conditional_ig
        TestBasic.igs[TestBasic.conditional_ig] = ig3_path
        self.igm.save_ig(ig3_path)
        self.assertIn(TestBasic.conditional_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_if_IG(self):
        # DEBUG REMOVE
        TestBasic.igs[TestBasic.conditional_ig] = TestBasic.out_folder + "ig3.ig"

        self.igm.load_ig(TestBasic.igs[TestBasic.conditional_ig])
        self.igm.run()
        self.assertEqual(TestBasic.memory_obj.get("count1"), "Yes")
        self.assertEqual(TestBasic.memory_obj.get("count2"), "No")
        self.assertEqual(TestBasic.memory_obj.get("count3"), "Yes")

    def tearDown(self):
        # noinspection PyAttributeOutsideInit
        self.igm = None


def main():
    ut.main()


if __name__ == "__main__":
    main()
