# system dependencies
import json
from flask import request, jsonify, Blueprint
from logging import Logger
from flask_injector import inject
from flask_cors import cross_origin

# local dependencies
from app import Dataset
from constants import Constants
constants = Constants()

dataset_mod = Blueprint("dataset_generator", __name__, )


@inject(dataset_handller=Dataset, logger=Logger)
@dataset_mod.route('/init', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def generator(dataset_handller, logger):
    """
    """
    response = None
    response_code = 200

    dataset = Dataset(logger)
    try:
        json_data = request.get_json(force=True)
        logger.info("New request on" + request.path + " with body " + str(json_data))
        response, response_code = dataset_handller.generator(json_data)

    except Exception as e:
        logger.error(msg=e, exc_info=True)
        response = constants.GLOBAL_ERROR_MESSAGE
        response_code = 500

    return jsonify(response), response_code
