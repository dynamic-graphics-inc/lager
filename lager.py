# -*- coding: utf-8 -*-
import os
import logging.config
import logging

__version__ = '0.3.0'

LAGER = None

LAGER_OPERATORS = {
    "-" : logging.DEBUG,
    "+" : logging.INFO,
    "*" : logging.WARN,
    "**": logging.ERROR,
    "%" : logging.CRITICAL
    }

class ConsoleFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param in record.msg
        if allow:
            record.msg = record.msg.replace(self.param, '')
        return allow

LAGER_ONTAP = {
    'version'                 : 1,
    'disable_existing_loggers': False,
    'formatters'              : {
        'simple':
            {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}},
    'filters'                 : {
        'console_filter': {
            '()'   : ConsoleFilter,
            'param': '__NO_CONSOLE__'
            }
        },
    'handlers'                : {
        'console_handler': {'class'    : 'logging.StreamHandler',
                            'filters'  : ['console_filter'],
                            'formatter': 'simple',
                            'level'    : 'DEBUG',
                            'stream'   : 'ext://sys.stdout'},
        'file_handler'   : {'backupCount': 20,
                            'class'      : 'logging.handlers.RotatingFileHandler',
                            'encoding'   : 'utf8',
                            'filename'   : 'lager.log',
                            'formatter'  : 'simple',
                            'level'      : 'DEBUG',
                            'maxBytes'   : 10485760},
        },
    'root'                    : {
        'handlers': [
            'console_handler',
            'file_handler'
            ],
        'level'   : 'DEBUG'},
    }

class Lager(logging.Logger):
    def __init__(self,
                 logging_cfg_dict=LAGER_ONTAP,
                 operator_cfg_dict=LAGER_OPERATORS,
                 env_key='LOG_CFG'):
        """Setup logging configuration
        """
        value = os.getenv(env_key, None)
        if value:
            path = value
            print(path)
        logging.config.dictConfig(logging_cfg_dict)
        self.log_ops = operator_cfg_dict

    @staticmethod
    def log(level, msg):
        logging.log(level, msg)

    def __add__(self, msg):
        Lager.log(self.log_ops['+'], msg)
        return self

    def __sub__(self, msg):
        Lager.log(self.log_ops['-'], msg)
        return self

    def __mul__(self, msg):
        Lager.log(self.log_ops['*'], msg)
        return self

    def __pow__(self, msg, modulo=None):
        Lager.log(self.log_ops['**'], msg)
        return self

    def __mod__(self, msg):
        Lager.log(self.log_ops['%'], msg)
        return self

    def __iadd__(self, msg):
        return self.__add__('{} __NO_CONSOLE__'.format(msg))

    def __isub__(self, msg):
        return self.__sub__('{} __NO_CONSOLE__'.format(msg))

    def __imul__(self, msg):
        return self.__mul__('{} __NO_CONSOLE__'.format(msg))

    def __ipow__(self, msg):
        return self.__pow__('{} __NO_CONSOLE__'.format(msg))

    def __imod__(self, msg):
        return self.__mod__('{} __NO_CONSOLE__'.format(msg))

# setup_logging()
if __name__ == '__main__':
    captains_log = Lager()

    captains_log + "NO CONSOLE info +"
    captains_log += "YES CONSOLE info +="

    captains_log - "NO CONSOLE debug -"
    captains_log -= "YES CONSOLE debug -="

    captains_log * "NO CONSOLE *"
    captains_log *= "YES CONSOLE *="

    captains_log ** "NO CONSOLE **"
    captains_log **= "YES CONSOLE **="

    captains_log % "NO CONSOLE %"
    captains_log %= "YES CONSOLE %="
