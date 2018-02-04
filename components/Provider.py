from abc import ABCMeta, abstractmethod


class BaseProvider(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def __str__(self):
        return self.provider_name()

    @abstractmethod
    def provider_name(self):
        return 'BaseProvider'
