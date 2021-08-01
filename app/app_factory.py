# system dependencies
import logging
from logging import Logger, Formatter

from flask import Flask, Blueprint, request, abort, Response
from flask_injector import FlaskInjector
from flask_cors import CORS
from flask_log_request_id import RequestID

# application depenencies
from app import YamlParser, Dataset, Model
from app.api import dataset_mod
from app.logging import ContextualFilter, StackdriverJsonFormatter
from constants import Constants

main_mod = Blueprint('', __name__)

class AppFactory:

    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        self.constants = Constants()
        self.model = Model()
        if AppFactory.__instance__ is None:
            AppFactory.__instance__ = self
        else:
            raise Exception("You can not create another AppFactory class. Use AppFactory.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not AppFactory.__instance__:
            AppFactory()
        return AppFactory.__instance__

    def build_app(self, environment):
        """
        RESTApi application builder
        """
        CONFIG = self.constants.APP_CONFIG

        app = Flask(__name__)
        RequestID(app)

        server_config = YamlParser.parse_config_file(CONFIG, 'server', load_env_vars=True)
        app.config['ACCESS_TOKEN'] = server_config['accessToken']
        cors = CORS(app, resources={r'/*': {"origins": '*'}})

        # format app logger
        log_format = ("%(utcnow)s\tl=%(levelname)s\tip=%(ip)s"
                    "\tm=%(method)s\turl=%(url)s\tmsg=%(message)s")

        # set logging level
        level = logging.DEBUG if environment == self.constants.TEST_ENV else logging.INFO
        app.logger.setLevel(level)

        try:
            formatter = StackdriverJsonFormatter(fmt=log_format)
            app.logger.info("Stackdriver logger is up!")
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(Formatter(log_format))
            stream_handler.addFilter(ContextualFilter(filter_name='add_conn_id', extra='123'))
            app.logger.addHandler(stream_handler)

        except Exception as e:
            app.logger.error("Cannot set stackdriver logging!")
            app.logger.info("Setted stream logger")
            app.logger.error(e)

        def configure(binder):
            binder.bind(
                Logger,
                app.logger
            )
            binder.bind(
                Dataset,
                Dataset(logger=app.logger)
            )

        app.register_blueprint(dataset_mod, url_prefix=self.constants.BASE_URL_DATASET)
        app.register_blueprint(main_mod, url_prefix='/')

        def validate_access_token():
            urls = request.url.split("/")
            if urls[-1] != 'healthcheck':
                if 'AI-Api-Token' in request.headers:
                    access_token = request.headers['AI-Api-Token']
                    if access_token != app.config['ACCESS_TOKEN']:
                        abort(403)
                else:
                    abort(403)
            else:
                abort(Response(status=200))

        app.before_request(validate_access_token)
        FlaskInjector(app=app, modules=[configure])

        return app, server_config, app.logger
