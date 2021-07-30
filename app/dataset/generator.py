import numpy as np
import pandas as pd
from sklearn.datasets import make_regression

class Dataset:
    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        if Dataset.__instance__ is None:
            Dataset.__instance__ = self
        else:
            raise Exception("You can not create another Dataset class. Use Dataset.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Dataset.__instance__:
            Dataset()
        else:
            Dataset.__instance__

    def generator(self):
        raise Exception("Not implemented yet!")