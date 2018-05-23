from abc import ABCMeta, abstractmethod
import os


class BaseMemory(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._queued_ig_path = None  # Queues an IG to be run with the run_ig built-in

    def __str__(self):
        return self.memory_name()

    def queue_ig_as_primitive(self, path):
        self._queued_ig_path = path

    def get_queued_ig(self):
        return self._queued_ig_path

    @abstractmethod
    def memory_name(self):
        return 'BaseMemory'
