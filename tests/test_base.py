import os
import unittest as ut
from glob import glob
from abc import abstractmethod, ABCMeta
from instruction_graph.example.DefaultMemory import DefaultMemory


class TestBase(ut.TestCase):
    out_folder = "generated/"  # WARNING: Test will delete .ig files from this folder before tests

    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def skip(cls):
        raise NotImplementedError()

    @classmethod
    def setUpClass(cls):
        if cls.skip():
            raise ut.SkipTest("DEBUG")
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
