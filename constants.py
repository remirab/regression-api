import os

def read_only_properties(*attrs):
    """
    Make attributes of a class readonly.
    """

    def class_rebuilder(cls):
        """
        The class decorator example
        """

        class NewClass(cls):
            """
            This is the overwritten class
            """
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


@read_only_properties(
    "LOG_FILE",
    "BASE_URL",
    "BASE_URL_REGRESSION",
    "DEV_ENV",
    "PROD_ENV",
    "TEST_ENV",
    "GLOBAL_ERROR_MESSAGE",
    "ROOT_DIR",
    "DATASETS_DIR",
    "IMAGES_DIR",
    "APP_CONFIG",
    "DATASET_PROP",
    "REGRESSOR",
    "JUPYTER"
)
class Constants:
    """
    All global constant parameters 
    """

    def __init__(self):
        """
        Constructor
        """
        # default log file
        self.LOG_FILE = "app.log"

        # base url for endpoints
        self.BASE_URL = "/regression-api/inference"
        self.BASE_URL_REGRESSION = self.BASE_URL + "/regression"

        # environments
        self.DEV_ENV = "DEV"
        self.PROD_ENV = "PROD"
        self.TEST_ENV = "TEST"

        # general error message
        self.GLOBAL_ERROR_MESSAGE = "Execution error!"

        # config files and important folders
        self.ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.DATASETS_DIR = self.ROOT_DIR + "/app/dataset/store/"
        self.IMAGES_DIR = self.ROOT_DIR + "/app/jupyter/images/"
        self.APP_CONFIG = self.ROOT_DIR + "/app/conf/config.yaml"

        # scikit-learn dataset generation params
        self.DATASET_PROP = {
            "n_samples": 100,
            "n_features": 2,
            "n_informative": 2,
            "n_targets": 1,
            "shuffle": True,
            "noise": 0.0,
            "coef": True,
            "rnd_state": 111
        }

        # regression model config
        self.REGRESSOR = "LinearRegression"

        # jupyter notebook run
        self.JUPYTER = True
