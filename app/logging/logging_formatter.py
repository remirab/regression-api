import sys
import json
import logging
from pythonjsonlogger import jsonlogger
from collections import OrderedDict

DEFAULT_LOGGER_NAME = "python"


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):

    def __init__(self, fmt="%(levelname) %(message)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):

        log_record['message'] = log_record['message']
        log_record['metadata']['requestUrl'] = log_record['url']
        log_record['metadata']['requestOrigin'] = log_record['ip']
        log_record['metadata']['requestMethod'] = log_record['method']
        log_record['metadata']['requestId'] = log_record['request_id']

        del log_record['request_id']
        del log_record['url']
        del log_record['ip']
        del log_record['method']

        return super(StackdriverJsonFormatter, self).process_log_record(log_record)

    def format(self, record):
        """Formats a log record"""

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        record_to_add = {
            'metadata': {
            }
        }

        if record.exc_text:
            record_to_add['metadata']['exc_info'] = record.exc_text

        self.add_fields(log_record, record, record_to_add)

        log_record = self.process_log_record(log_record)
        return log_record
