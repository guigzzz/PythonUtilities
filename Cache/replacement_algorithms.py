from abc import ABCMeta, abstractclassmethod
from collections import OrderedDict

class ReplacementPrototype(metaclass = ABCMeta):
    """
    Prototype class for the replacement policies.
    Classes that inherit from this class must reimplement all the functions
    decorated with @abstrastclassmethod.
    """
    def __init__(self):
        pass

    @abstractclassmethod
    def select_pop_item(self):
        pass

    @abstractclassmethod
    def update_on_write(self, key):
        return None

    @abstractclassmethod
    def update_on_read(self):
        return None

class MRU(ReplacementPrototype):
    """ Most Recently Used replacement strategy """
    def __init__(self):
        self.__most_recent = None

    def select_pop_item(self):
        return self.__most_recent

    def update_on_read(self, key, value):
        if value is not None:
            self.__most_recent = key

    def update_on_write(self, key, value):
        self.__most_recent = key
        

class LRU(ReplacementPrototype):
    """ Least Recently Used replacement strategy """
    def __init__(self):
        self.__orderdict = OrderedDict()

    def select_pop_item(self):
        popped_key = next(iter(self.__orderdict.items()))[0]
        self.__orderdict.pop(popped_key)
        return popped_key

    def update_on_read(self, key, value):
        if value is not None:
            self.__orderdict.move_to_end(key)

    def update_on_write(self, key, value):
        self.__orderdict[key] = 0 # no need to store actual value
