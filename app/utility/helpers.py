# system dependencies
import string
import random

# local dependencies
from constants import Constants

class Helpers:
    """
    helper functions
    """

    def __init__(self):
        self.constants = Constants()
        random.seed(self.constants.RND_STATE)

    def random_character(self):
        return random.choice(string.ascii_lowercase)

    @staticmethod
    def read_only_properties(*attrs):
        """
        Make attributes of a class readonly.

        >>> @read_only_properties('readonly', 'forbidden')
        >>> class MyClass(object):
        ... def __init__(self, a, b, c):
        ...     self.readonly = a
        ...     self.forbidden = b

        >>> m = MyClass(1, 2, 3)
        >>> m.ok = 3
        >>> print(m.ok, m.readonly)

        # can touch ok
        >>> print("This worked...")
        # this will explode
        >>> m.forbidden = 4
        """

        def class_rebuilder(cls):
            "The class decorator example"

            class NewClass(cls):
                "This is the overwritten class"
                def __setattr__(self, name, value):

                    if name not in attrs:
                        pass
                    elif name not in self.__dict__:
                        pass
                    else:
                        raise AttributeError("Can't touch {}".format(name))

                    super().__setattr__(name, value)

            return NewClass

        return class_rebuilder
