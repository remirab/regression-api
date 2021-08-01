import logging
import datetime
from flask import request
from flask_log_request_id import current_request_id


class ContextualFilter(logging.Filter):

    def __init__(self, filter_name, extra):
        super(ContextualFilter, self).__init__(filter_name)
        self.connid = extra

    def filter(self, log_record):

        """ Provide some extra variables to give our logs some
        better info """

        log_record.utcnow = (datetime.datetime.utcnow()
                            .strftime('%Y-%m-%d %H:%M:%S,%f %Z'))
        try:

            log_record.url = request.path
            log_record.method = request.method
            # Try to get the IP address of the user through reverse proxy
            log_record.ip = request.environ.get('HTTP_X_REAL_IP',
                                  request.remote_addr)

            log_record.request_id = current_request_id()



        except Exception as e:
            log_record.url = "Unkknown"
            log_record.method = "Unkknown"
            log_record.ip = "Unkknown"
            log_record.id = "Unknown"
            log_record.request_id = "Unknown"

        return True
