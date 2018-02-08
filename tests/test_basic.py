import os
import unittest as ut
from glob import glob

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instruction_graph.core.Manager import Manager
from instruction_graph.example.DefaultProvider import DefaultProvider

from instruction_graph.example.ExamplePrimitiveLibrary import ExamplePrimitiveLibrary


class TestBasic(ut.TestCase):

    provider = None
    out_folder = "generated/"  # WARNING: Test will delete .ig files from this folder before tests
    igs = {}

    simple_ig = "ig1.ig"
    loop_ig = "ig2.ig"
    conditional_ig = "ig3.ig"

    @classmethod
    def setUpClass(cls):
        cls.provider = DefaultProvider()
        cls.igs = {}
        del_path = cls.out_folder + "*.ig"
        for f in glob(del_path):
            os.remove(f)
            pass

    @classmethod
    def tearDownClass(cls):
        # optionally, delete stuff in generated. for now, doing it just in setup so can
        #   view igs after creation
        # os.remove(glob(cls.out_folder + '*.ig'))
        pass

    def setUp(self):
        TestBasic.provider = DefaultProvider()
        library = ExamplePrimitiveLibrary()
        # noinspection PyAttributeOutsideInit
        self.igm = Manager(library=library, provider=TestBasic.provider)

    def test_create_and_save_simple_IG(self):
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_zero", args=["Action 1"], pass_provider=False)
        self.igm.ig.add_action("fun_hello")
        self.igm.ig.add_action("fun_zero", args=["Action 3"])
        self.igm.ig.add_action("fun_hello")
        self.igm.ig.add_action("fun_set", args=["key1", "val1"], pass_provider=True)
        ig1_name = TestBasic.simple_ig
        ig1_path = TestBasic.out_folder + ig1_name
        TestBasic.igs[TestBasic.simple_ig] = ig1_path
        self.igm.save_ig(ig1_path)
        self.assertIn(ig1_name, os.listdir(TestBasic.out_folder))

    def test_load_and_run_simple_IG(self):
        self.igm.load_ig(TestBasic.igs[TestBasic.simple_ig])
        self.igm.run()
        self.assertEquals(TestBasic.provider.get("key1"), "val1")

    def test_create_and_save_cond_loop_IG(self):
        ct = "count"
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=[ct, 0], pass_provider=True)
        self.igm.ig.add_loop('less', args=[ct, 4], pass_provider=True)
        self.igm.ig.add_action("inc", args=[ct], pass_provider=True)
        self.igm.ig.add_end_loop()
        ig2_path = TestBasic.out_folder + TestBasic.loop_ig
        TestBasic.igs[TestBasic.loop_ig] = ig2_path
        self.igm.save_ig(ig2_path)
        self.assertIn(TestBasic.loop_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_loop_IG(self):
        self.igm.load_ig(TestBasic.igs[TestBasic.loop_ig])
        self.igm.run()
        self.assertEqual(TestBasic.provider.get("count"), 4)

    def test_create_and_save_cond_if_IG(self):
        ct = "count1"
        ct2 = "count2"
        ct3 = "count3"
        self.igm.create_new_ig()
        self.igm.ig.add_action("fun_set", args=[ct, 0], pass_provider=True)
        self.igm.ig.add_action("fun_set", args=[ct2, 10], pass_provider=True)
        self.igm.ig.add_action("fun_set", args=[ct3, 10], pass_provider=True)

        self.igm.ig.add_if('less', args=[ct, 4], pass_provider=True)
        self.igm.ig.add_action("fun_set", args=[ct, "Yes"], pass_provider=True)
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct, "No"], pass_provider=True)
        self.igm.ig.add_end_if()

        self.igm.ig.add_if('less', args=[ct2, 4], pass_provider=True, negation=False)
        self.igm.ig.add_action("fun_set", args=[ct2, "Yes"], pass_provider=True)
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct2, "No"], pass_provider=True)
        self.igm.ig.add_end_if()

        self.igm.ig.add_if('less', args=[ct3, 4], pass_provider=True, negation=True)
        self.igm.ig.add_action("fun_set", args=[ct3, "Yes"], pass_provider=True)
        self.igm.ig.add_else()
        self.igm.ig.add_action("fun_set", args=[ct3, "No"], pass_provider=True)
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
        self.assertEqual(TestBasic.provider.get("count1"), "Yes")
        self.assertEqual(TestBasic.provider.get("count2"), "No")
        self.assertEqual(TestBasic.provider.get("count3"), "Yes")

    def tearDown(self):
        # noinspection PyAttributeOutsideInit
        self.igm = None


def main():
    ut.main()

if __name__ == "__main__":
    main()
