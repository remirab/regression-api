# system dependencies
import os
import logging
logger = logging.getLogger("main")

# local dependencies
from app import AppFactory


if __name__ == "__main__":
    try:
        # instantiate app factory
        app_factory = AppFactory.get_instance()

        # load config and env variables
        environment = os.getenv('ENV') if os.getenv('ENV') is not None else 'DEV'
        app, server_config, logger = app_factory.build_app(environment)
        host, port = server_config['host'], server_config['port']
        logger.info("App started!")
        logger.info(f'Starting with APP={app}, HOST={host}, PORT={port}, LOGGER={logger}')
        app.run()

    except Exception as e:
        logger.error("Regression API service did not start properly!")
        logger.error(e, exc_info=True)
