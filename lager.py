import os
from pprint import pprint
import functools
from os import path
import logging.config
import logging
import yaml
from functools import wraps

LOG_OPERATORS = {
    "-": logging.DEBUG,
    "+": logging.INFO,
    "*": logging.WARN,
    "**": logging.ERROR,
    "%": logging.CRITICAL
}
# logging.config.dictConfig({
LAGER_ONTAP = {'disable_existing_loggers': False,
               'formatters': {'simple': {'format': '%(asctime)s - %(name)s - %(levelname)s - '
                                                   '%(message)s'}},
               'handlers': {'console': {'class': 'logging.StreamHandler',
                                        'formatter': 'simple',
                                        'level': 'DEBUG',
                                        'stream': 'ext://sys.stdout'},
                            'error_file_handler': {'backupCount': 20,
                                                   'class': 'logging.handlers.RotatingFileHandler',
                                                   'encoding': 'utf8',
                                                   'filename': 'E.log',
                                                   'formatter': 'simple',
                                                   'level': 'ERROR',
                                                   'maxBytes': 10485760},
                            'info_file_handler': {'backupCount': 20,
                                                  'class': 'logging.handlers.RotatingFileHandler',
                                                  'encoding': 'utf8',
                                                  'filename': 'I.log',
                                                  'formatter': 'simple',
                                                  'level': 'INFO',
                                                  'maxBytes': 10485760}},
               'loggers': {'my_module': {'handlers': ['console'],
                                         'level': 'ERROR',
                                         'propagate': False}},
               'root': {'handlers': ['console', 'info_file_handler', 'error_file_handler'],
                        'level': 'INFO'},
               'version': 1}

class Lager:
    def __init__(self,
                 default_log_level=logging.INFO,
                 env_key='LOG_CFG'):
        """Setup logging configuration
        """
        value = os.getenv(env_key, None)
        if value:
            path = value
            print(path)
        logging.config.dictConfig(LAGER_ONTAP)
        # else:
        #     logging.basicConfig(level=default_log_level)

    @staticmethod
    def log(level, msg):
        logging.log(level, msg)

    def __add__(self, msg: str):
        self.log(logging.INFO, msg)
        return self

    def __isub__(self, msg: str):
        """Pretty slick way of logging
        :param msg:
        :return:
        """
        logging.info(msg)
        return self

    def __imul__(self, error_msg: str):
        logging.error(error_msg)
        return self

    def debug(self, msg):
        logging.debug(msg)


# setup_logging()
frog: Lager = Lager()
frog += "yay this is the log"
frog -= "yay this is the log"
frog -= 'this is also a log'
