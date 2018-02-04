import os
from glob import glob
import unittest as ut
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Manager import Manager
import example.init_example as einit
from example.DefaultProvider import DefaultProvier


class TestBasic(ut.TestCase):

    provider = None
    out_folder = "generated/"  # WARNING: Test will delete .ig files from this folder before tests
    igs = {}

    simple_ig = "ig1.ig"
    loop_ig = "ig2.ig"
    conditional_ig = "ig3.ig"

    @classmethod
    def setUpClass(cls):
        cls.provider = DefaultProvier()
        cls.igs = {}
        del_path = cls.out_folder + "*.ig"
        for f in glob(del_path):
            os.remove(f)

    @classmethod
    def tearDownClass(cls):
        # optionally, delete stuff in generated. for now, doing it just in setup so can
        #   view igs after creation
        # os.remove(glob(cls.out_folder + '*.ig'))
        pass

    def setUp(self):
        # noinspection PyAttributeOutsideInit
        self.igm = Manager()
        self.igm.init_robot(einit.fn_dict, einit.fn_store_name, provider=TestBasic.provider)

    def test_create_and_save_simple_IG(self):
        self.igm.createNewIG()
        self.igm.ig.addAction("fun_zero", args=["Action 1"], pass_provider=False)
        self.igm.ig.addAction("fun_hello")
        self.igm.ig.addAction("fun_zero", args=["Action 3"])
        self.igm.ig.addAction("fun_hello")
        self.igm.ig.addAction("fun_set", args=["key1", "val1"], pass_provider=True)
        ig1_name = TestBasic.simple_ig
        ig1_path = TestBasic.out_folder + ig1_name
        TestBasic.igs[TestBasic.simple_ig] = ig1_path
        self.igm.saveIG(ig1_path)
        self.assertIn(ig1_name, os.listdir(TestBasic.out_folder))

    def test_load_and_run_simple_IG(self):
        self.igm.loadIG(TestBasic.igs[TestBasic.simple_ig])
        self.igm.run()
        self.assertEquals(TestBasic.provider.get("key1"), "val1")

    def test_create_and_save_cond_loop_IG(self):
        ct = "count"
        self.igm.createNewIG()
        self.igm.ig.addAction("fun_set", args=[ct, 0], pass_provider=True)
        self.igm.ig.addLoop('less', args=[ct, 4], pass_provider=True)
        self.igm.ig.addAction("inc", args=[ct], pass_provider=True)
        self.igm.ig.addEndLoop()
        ig2_path = TestBasic.out_folder + TestBasic.loop_ig
        TestBasic.igs[TestBasic.loop_ig] = ig2_path
        self.igm.saveIG(ig2_path)
        self.assertIn(TestBasic.loop_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_loop_IG(self):
        self.igm.loadIG(TestBasic.igs[TestBasic.loop_ig])
        self.igm.run()
        self.assertEqual(TestBasic.provider.get("count"), 4)

    def test_create_and_save_cond_if_IG(self):
        ct = "count1"
        ct2 = "count2"
        self.igm.createNewIG()
        self.igm.ig.addAction("fun_set", args=[ct, 0], pass_provider=True)
        self.igm.ig.addAction("fun_set", args=[ct2, 10], pass_provider=True)
        self.igm.ig.addIf('less', args=[ct, 4], pass_provider=True)
        self.igm.ig.addAction("fun_set", args=[ct, "Yes"], pass_provider=True)
        self.igm.ig.addElse()
        self.igm.ig.addAction("fun_set", args=[ct, "No"], pass_provider=True)
        self.igm.ig.addEndIf()
        self.igm.ig.addIf('less', args=[ct2, 4], pass_provider=True)
        self.igm.ig.addAction("fun_set", args=[ct2, "Yes"], pass_provider=True)
        self.igm.ig.addElse()
        self.igm.ig.addAction("fun_set", args=[ct2, "No"], pass_provider=True)
        self.igm.ig.addEndIf()
        ig3_path = TestBasic.out_folder + TestBasic.conditional_ig
        TestBasic.igs[TestBasic.conditional_ig] = ig3_path
        self.igm.saveIG(ig3_path)
        self.assertIn(TestBasic.conditional_ig, os.listdir(TestBasic.out_folder))

    def test_load_and_run_cond_if_IG(self):
        self.igm.loadIG(TestBasic.igs[TestBasic.conditional_ig])
        self.igm.run()
        self.assertEqual(TestBasic.provider.get("count1"), "Yes")
        self.assertEqual(TestBasic.provider.get("count2"), "No")

    def tearDown(self):
        # noinspection PyAttributeOutsideInit
        self.igm = None


def main():
    ut.main()

if __name__ == "__main__":
    main()

### Note: apply object to args (so ACTuples can be used like functions)  then make a FunctionStore abstract base class
### Note: for lp, do a functional iteration through the ACTuples for searching for words (use filter)
