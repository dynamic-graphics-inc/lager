# -*- coding: utf-8 -*-
"""
EZ PZ logging
"""
import logging
import os
import sys
from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import FileHandler
from logging import INFO
from logging import StreamHandler
from logging import WARNING
from logging import handlers

from colorama import Fore
from rapidjson import dumps
from rapidjson import loads
from structlog import configure
from structlog import threadlocal
from structlog import processors
from structlog import stdlib

try:
    import curses
except ImportError:
    curses = None

if os.name == "nt":
    from colorama import init as colorama_init

    colorama_init()
_CONFIGURED = False
_LOG_FILE = None
_LOG_LEVELS = {
    "debug"   : DEBUG,
    "d"       : DEBUG,
    "info"    : INFO,
    "i"       : INFO,
    "warning" : WARNING,
    "w"       : WARNING,
    "error"   : ERROR,
    "e"       : ERROR,
    "critical": CRITICAL,
    "c"       : CRITICAL,
    }
LAGERS = {}
DATE_FMT = "%y%m%dT%H:%M:%S"
RECORD_KEYS = [
    "name",
    "time",
    "level",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "logger",
    "timestamp",
    "asctime",
    "color",
    "end_color",
    ]

FILTER = {
    "created",
    "exc_info",
    "filename",
    "levelno",
    "exc_text",
    "stack_info",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "logger",
    "args",
    "timestamp",
    "end_color",
    "color",
    "levelname",
    }
KEEP = [k for k in RECORD_KEYS if k not in FILTER]
BASE_LOGGER_NAME = 'LAGER'
colorify = "{}{}{}".format
colors = {
    "d": Fore.CYAN,
    "i": Fore.GREEN,
    "w": Fore.YELLOW,
    "e": Fore.RED,
    "D": Fore.CYAN,
    "I": Fore.GREEN,
    "W": Fore.YELLOW,
    "E": Fore.RED
    }

configure(
    context_class=threadlocal.wrap_dict(dict),
    logger_factory=stdlib.LoggerFactory(),
    wrapper_class=stdlib.BoundLogger,
    processors=[
        stdlib.filter_by_level,
        stdlib.add_logger_name,
        stdlib.add_log_level,
        stdlib.PositionalArgumentsFormatter(),
        processors.TimeStamper(fmt="iso"),
        processors.StackInfoRenderer(),
        processors.format_exc_info,
        processors.UnicodeDecoder(),
        stdlib.render_to_log_kwargs,
        ],
    )

def _stderr_colorable():
    if os.name == "nt":
        return True
    if curses and hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                return True

        except Exception:
            pass

    return False

class LagerFormatter(logging.Formatter):
    def __init__(self, color=True):
        self.color = color
        logging.Formatter.__init__(self, datefmt=DATE_FMT)

    def _dict(self, record):
        _msg = {
            k: v for k, v in record.__dict__.items() if k not in RECORD_KEYS
            }
        _other = {
            k: v
            for k, v in record.__dict__.items()
            if k in RECORD_KEYS and k not in FILTER
            }
        return {**_msg, **_other}

    def format(self, record):
        print(record, dir(record))
        record.time = self.formatTime(record, self.datefmt)
        formatted = dumps(self._dict(record))
        if self.color:
            # formatted = colorify(colors[record.level[0]], formatted, Fore.WHITE)
            formatted = colorify(colors[record.levelname[0]], formatted, Fore.WHITE)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        return formatted

def pour_lager(
    name=None,
    filepath=None,
    level=DEBUG,
    stderr=True,
    maxBytes=None,
    logfile_mode="a",
    ):
    if isinstance(level, str):
        try:
            level = _LOG_LEVELS[level.lower()]
        except KeyError as e:
            log_level_strings = ", ".join(_LOG_LEVELS.keys())
            raise ValueError(
                "Valid string log levels are: {}".format(log_level_strings)
                )
    elif level not in _LOG_LEVELS.values():
        raise ValueError("Not a valid log_level")

    _name = (name or __name__)
    _logger = logging.getLogger(_name)
    if stderr:
        c_handler = StreamHandler()
        c_handler.setLevel(level)
        c_handler.setFormatter(LagerFormatter(color=_stderr_colorable()))
        _logger.addHandler(c_handler)
    if filepath:
        _lager_formatter = LagerFormatter(color=False)
        if maxBytes:
            f_handler = handlers.RotatingFileHandler(
                filepath, maxBytes=maxBytes
                )
        else:
            f_handler = FileHandler(filepath, mode=logfile_mode)
        f_handler.setLevel(level)
        f_handler.setFormatter(_lager_formatter)
        _logger.addHandler(f_handler)
    _logger.propagate = False
    _logger.setLevel(level)
    return logging.getLogger(_name)

def find_lager(name=__name__):
    if LAGERS.get(name):
        return LAGERS.get(name)

    logger = pour_lager(name=name)
    LAGERS[name] = logger
    return logger

def load_log(filepath):
    with open(filepath, 'r') as f:
        data = f.read().splitlines(keepends=False)
    return [loads(l) for l in data]

if __name__ == "__main__":
    pass
    # from doctest import testmod
    # testmod()
