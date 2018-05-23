import os
import unittest as ut
from glob import glob

from instruction_graph.example.DefaultMemory import DefaultMemory


class TestBase(ut.TestCase):
    out_folder = "generated/"  # WARNING: Test will delete .ig files from this folder before tests

    @classmethod
    def setUpClass(cls):
        print("setup is running")
        cls.memory_obj = DefaultMemory()
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
