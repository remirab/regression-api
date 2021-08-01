from app.dataset import Dataset
from app.model import Model
from app.utility import YamlParser, Helpers
from app.app_factory import AppFactory

__all__ = ["Dataset", "Model", "YamlParser", "Helpers", "AppFactory"]


import os
from constants import Constants
constants = Constants()

if not os.path.exists(constants.JUPYTER_DIR):
    os.mkdir(constants.JUPYTER_DIR)

if not os.path.exists(constants.DATASETS_DIR):
    os.mkdir(constants.DATASETS_DIR)

if not os.path.exists(constants.IMAGES_DIR):
    os.mkdir(constants.IMAGES_DIR)
