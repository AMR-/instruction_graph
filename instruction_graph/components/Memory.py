from abc import ABCMeta, abstractmethod


class BaseMemory(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def __str__(self):
        return self.memory_name()

    @abstractmethod
    def memory_name(self):
        return 'BaseMemory'
