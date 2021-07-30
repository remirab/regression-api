from sklearn.linear_model import LinearRegression, BayesianRidge, ARDRegression, LogisticRegression, HuberRegressor, Ridge

class Model:
    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        if Model.__instance__ is None:
            Model.__instance__ = self
        else:
            raise Exception("You can not create another Model class. Use Model.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Model.__instance__:
            Model()
        else:
            Model.__instance__

    def maker(self):
        raise Exception("Not implemented yet!")

    def trainer(self):
        raise Exception("Not implemented yet!")

    def predictor(self):
        raise Exception("Not implemented yet!")
