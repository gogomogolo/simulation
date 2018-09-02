from abc import ABCMeta, abstractmethod


class BooleanExpressionMinimizer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def minimize(self): pass
