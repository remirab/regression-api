# system dependencies
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression
from flask import request
import pickle

# local dependencies
from constants import Constants
from app.utility import Helpers


class Dataset:

    def __init__(self, logger):
        """
        Constructor
        """
        self.constants = Constants()
        self.helpers = Helpers()
        self.dataset_properties = self.constants.DATASET_PROP
        self.logger = logger

    def generator(self, json_data):
        """
        """

        response = "OK"
        response_code = 200

        try:
            self.logger.info("New request on" + request.path + " with body " + str(json_data))
            # generate raw dataset
            d_frame = self.dataset_generator(self.constants.DATASET_PROP)
            # insert alphabet column
            d_frame = self.insert_alphabet_column(dataframe=d_frame, idx=self.constants.DATASET_PROP["n_features"])
            # save dataframe to pickle file
            self.save_dataset(dataframe=d_frame, path=self.constants.DATASETS_DIR)
            response = "Dataset successfully generated!"

        except Exception as e:
            self.logger.error(e, exc_info=True)
            response = self.constants.GLOBAL_ERROR_MESSAGE
            response_code = 500

        return response, response_code

    def save_dataset(self, dataframe: pd.DataFrame, path: str):
        file_name = path + "/dataset.pkl"
        dataframe.to_pickle(path=file_name)

    def load_dataset(self, file_name: str, path: str):
        file_path = path + file_name
        return pd.read_pickle(filepath_or_buffer=file_path)

    def insert_alphabet_column(self, dataframe: pd.DataFrame, idx: int):
        column_name = f"feature_{eval(list(dataframe.columns.values)[-2].split('_')[1]) + 1}"
        dataframe.insert(loc=idx, column=column_name, value=[self.helpers.random_character() for _ in range(dataframe.shape[0])])
        return dataframe

    def dataset_generator(self, dataset_properties: dict):
        X, y = make_regression(
            n_samples=dataset_properties["n_samples"],
            n_features=dataset_properties["n_features"],
            n_informative=dataset_properties["n_informative"],
            n_targets=dataset_properties["n_targets"],
            shuffle=dataset_properties["shuffle"],
            noise=dataset_properties["noise"],
            random_state=dataset_properties["rnd_state"]
        )
        columns = [f"feature_{i}" for i in range(dataset_properties["n_features"])]
        columns.append("target")
        return pd.DataFrame(data=np.c_[X, y], columns=columns)
