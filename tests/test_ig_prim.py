import os
# import unittest as ut
from test_base import TestBase

from instruction_graph.core.Manager import Manager
from instruction_graph.example.DefaultMemory import DefaultMemory

from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestRunIG(TestBase):

    memory_obj = None
    igs = {}

    prim1_ig = "ig_ri1.ig"
    prim2_ig = "ig_ri2.ig"
    top_parent_ig = "ig_ri3.ig"
    top_parent_ig_rev = "ig_ri4.ig"

    parent_dynamic_ig = "ig_ri5.ig"

    top_parent_two_level_ig = "ig_ri7.ig"

    def setUp(self):
        # raise ut.SkipTest("DEBUG")
        TestRunIG.memory_obj = DefaultMemory()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit
        self.igm = Manager(library=library, memory=TestRunIG.memory_obj)

    def test_create_and_save_nested_IGs(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_zero", args=["Action 1"], pass_memory_obj=False)
        self.igm.ig.add_action("fun_hello", pass_memory_obj=False)
        self.igm.ig.add_action("fun_set", args=["key1", "val1"])
        self.igm.ig.add_action("fun_set", args=["1_run", "true"])
        ig1_name = TestRunIG.prim1_ig
        ig1_path = TestRunIG.out_folder + ig1_name
        TestRunIG.igs[TestRunIG.prim1_ig] = ig1_path
        self.igm.save_ig(ig1_path)
        self.assertIn(ig1_name, os.listdir(TestRunIG.out_folder))

        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=["key1", "val2"])
        self.igm.ig.add_action("fun_set", args=["2_run", "true"])
        ig2_name = TestRunIG.prim2_ig
        ig2_path = TestRunIG.out_folder + ig2_name
        TestRunIG.igs[TestRunIG.prim2_ig] = ig2_path
        self.igm.save_ig(ig2_path)
        self.assertIn(ig2_name, os.listdir(TestRunIG.out_folder))

        self.igm.create_new_ig()
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig1_path])
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig2_path])
        top_parent_ig_name = TestRunIG.top_parent_ig
        top_parent_ig_path = TestRunIG.out_folder + top_parent_ig_name
        TestRunIG.igs[TestRunIG.top_parent_ig] = top_parent_ig_path
        self.igm.save_ig(top_parent_ig_path)
        self.assertIn(top_parent_ig_name, os.listdir(TestRunIG.out_folder))

        self.igm.create_new_ig()
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig2_path])
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig1_path])
        top_parent_ig_rev_name = TestRunIG.top_parent_ig_rev
        top_parent_ig_rev_path = TestRunIG.out_folder + top_parent_ig_rev_name
        TestRunIG.igs[TestRunIG.top_parent_ig_rev] = top_parent_ig_rev_path
        self.igm.save_ig(top_parent_ig_rev_path)
        self.assertIn(top_parent_ig_rev_name, os.listdir(TestRunIG.out_folder))

        # Dynamically set run_ig
        self.igm.create_new_ig()
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig2_path])
        self.igm.ig.add_action("queue_ig", args=[ig1_path])
        self.igm.ig.add_action(self.igm.library.run_ig_name)
        dynamic_parent_ig_name = TestRunIG.parent_dynamic_ig
        dyanmic_parent_ig_path = TestRunIG.out_folder + dynamic_parent_ig_name
        TestRunIG.igs[TestRunIG.parent_dynamic_ig] = dyanmic_parent_ig_path
        self.igm.save_ig(dyanmic_parent_ig_path)
        self.assertIn(dynamic_parent_ig_name, os.listdir(TestRunIG.out_folder))

        # Multi-Level run_ig
        self.igm.create_new_ig()
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[ig1_path])
        self.igm.ig.add_action(self.igm.library.run_ig_name, args=[top_parent_ig_path])
        two_level_ig_name = TestRunIG.top_parent_two_level_ig
        two_level_ig_path = TestRunIG.out_folder + two_level_ig_name
        TestRunIG.igs[TestRunIG.top_parent_two_level_ig] = two_level_ig_path
        self.igm.save_ig(two_level_ig_path)
        self.assertIn(two_level_ig_name, os.listdir(TestRunIG.out_folder))

    def test_load_and_run_prim_IG_alone(self):
        self.igm.load_ig(TestRunIG.igs[TestRunIG.prim1_ig])
        self.igm.run()
        self.assertEquals(TestRunIG.memory_obj.get("key1"), "val1")
        self.assertEquals(TestRunIG.memory_obj.get("1_run"), "true")

    def test_load_and_run_IG_with_ig_prims(self):
        self.igm.load_ig(TestRunIG.igs[TestRunIG.top_parent_ig])
        self.igm.run()
        self.assertEquals(TestRunIG.memory_obj.get("key1"), "val2")
        self.assertEquals(TestRunIG.memory_obj.get("1_run"), "true")
        self.assertEquals(TestRunIG.memory_obj.get("2_run"), "true")

    def test_load_and_run_IG_with_ig_prims_reverse(self):
        self.igm.load_ig(TestRunIG.igs[TestRunIG.top_parent_ig_rev])
        self.igm.run()
        self.assertEquals(TestRunIG.memory_obj.get("key1"), "val1")
        self.assertEquals(TestRunIG.memory_obj.get("1_run"), "true")
        self.assertEquals(TestRunIG.memory_obj.get("2_run"), "true")

    def test_load_and_run_IG_with_dynamic_ig_prims(self):
        self.igm.load_ig(TestRunIG.igs[TestRunIG.parent_dynamic_ig])
        self.igm.run()
        self.assertEquals(TestRunIG.memory_obj.get("key1"), "val1")
        self.assertEquals(TestRunIG.memory_obj.get("1_run"), "true")
        self.assertEquals(TestRunIG.memory_obj.get("2_run"), "true")

    def test_load_and_run_IG_with_two_layer_ig_prims(self):
        self.igm.load_ig(TestRunIG.igs[TestRunIG.top_parent_two_level_ig])
        self.igm.run()
        self.assertEquals(TestRunIG.memory_obj.get("key1"), "val2")
        self.assertEquals(TestRunIG.memory_obj.get("1_run"), "true")
        self.assertEquals(TestRunIG.memory_obj.get("2_run"), "true")
