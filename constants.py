import os

def readonly(value):
    return property(lambda self: value)

class Constants:

    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        if Constants.__instance__ is None:
            Constants.__instance__ = self
        else:
            raise Exception("You can not create another Constants class. Use Constants.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Constants.__instance__:
            Constants()
        return Constants.__instance__

    # default log file
    LOG_FILE = readonly("app.log")

    # base url for endpoints
    BASE_URL = readonly("/rigid-robotics/ai/inference")
    BASE_URL_REGRESSION = readonly(BASE_URL + "/regression")

    # environments
    DEV_ENV = readonly("DEV")
    PROD_ENV = readonly("PROD")

    # general error message
    GLOBAL_ERROR_MESSAGE = readonly("Execution error!")

    # config files
    ROOT_DIR = readonly(os.path.dirname(os.path.realpath(__file__)))
    APP_CONFIG = readonly(os.path.dirname(os.path.realpath(__file__)) + "/app/conf/config.yaml")

    # dataset generation params
    N_SAMPLES = readonly(100000)
    N_FEATURES = readonly(3)
    N_INFORMATIVE = readonly(3)
    N_TARGETS = readonly(1)
    SHUFFLE = readonly(True)
    NOISE = readonly(0.0)
    COEF = readonly(True)

    # regression model config
    REGRESSOR = readonly("LinearRegression")
