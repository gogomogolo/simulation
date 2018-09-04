from abc import ABCMeta, abstractmethod


class Distribution(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sample(self): pass

    @abstractmethod
    def pf(self): pass
