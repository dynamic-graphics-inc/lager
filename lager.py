# -*- coding: utf-8 -*-
"""
python lager ~ a new craft beer
"""
import os
import logging
import inspect
from inspect import getmodule
from inspect import stack
from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARNING
from logging import FileHandler, getLoggerClass, setLoggerClass
from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from logging import handlers
from logging import root
from os import name as osname
from sys import stderr as _stderr
from jsonbourne import json

try:
    import curses
except ImportError:
    curses = None

_COLOR = False

try:
    from colorama import Fore

    if osname == "nt":
        from colorama import init as colorama_init

        colorama_init()

    _COLORS = {
        "d": Fore.CYAN,
        "i": Fore.GREEN,
        "w": Fore.YELLOW,
        "e": Fore.RED,
        "c": Fore.MAGENTA,
        "D": Fore.CYAN,
        "I": Fore.GREEN,
        "W": Fore.YELLOW,
        "E": Fore.RED,
        "C": Fore.MAGENTA,
    }
    _COLOR = True
except (ModuleNotFoundError, ImportError):
    pass


def _stderr_colorable():
    if osname == "nt":
        return True
    if curses and hasattr(_stderr, "isatty") and _stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                return True

        except Exception:
            pass

    return False


_CONFIGURED = False
_LOG_FILE = None
_LOG_LEVELS = {
    "debug": DEBUG,
    "d": DEBUG,
    "info": INFO,
    "i": INFO,
    "warning": WARNING,
    "w": WARNING,
    "error": ERROR,
    "e": ERROR,
    "critical": CRITICAL,
    "c": CRITICAL,
}
_IS_LAGER = "_IS_LAGER"
DATE_FMT = "%y%m%dT%H:%M:%S"
TORNADO = "{color}[{levelname[0]} {asctime} {module}:{lineno}]{end_color} {msg}"

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


def _record_dict(record):
    _msg = {k: v for k, v in record.__dict__.items() if k not in RECORD_KEYS}

    _other = {
        k: v
        for k, v in record.__dict__.items()
        if k in RECORD_KEYS and k not in FILTER
    }
    return {**_msg, **_other}


def _json_record_dict(record):
    return {
        "who": f"{record.levelname[0]}:{record.name}",
        "when": record.time,
        "where": f"{record.module}:{record.lineno}",
        "what": record.msg,
    }


class LagerFormatter(Formatter):
    """Lager log formatter"""

    wwww = False

    def __init__(self, color=_COLOR, tornado=False, wwww=False):
        """Formatter constructor"""
        self.color = color
        self.tornado = tornado
        Formatter.__init__(self, datefmt=DATE_FMT)
        self.wwww = wwww
        self.format = (
            self.tornado_format
            if tornado
            else self.json_format_wwww
            if self.wwww
            else self.json_format
        )

    def tornado_format(self, record):
        """Format with tornado format"""
        record.time = self.formatTime(record, self.datefmt)
        record.asctime = self.formatTime(record, DATE_FMT)
        if self.color and _COLOR:
            record.color = _COLORS[record.levelname[0]]
            record.end_color = Fore.WHITE
        else:
            record.color = record.end_color = ""
        formatted = TORNADO.format_map(record.__dict__)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        return formatted.replace("\n", "\n    ")

    def json_format(self, record):
        """Format as json"""
        record.time = self.formatTime(record, self.datefmt)
        if record.module == "__main__":
            record.module = f"{record.pathname}::__main__"
        formatted = json.dumps(record.__dict__)
        if self.color and _COLOR:
            formatted = "".join(
                (_COLORS[record.levelname[0]], formatted, Fore.WHITE)
            )
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        return formatted

    def json_format_wwww(self, record):
        """Format as json"""
        record.time = self.formatTime(record, self.datefmt)
        if record.module == "__main__":
            record.module = f"{record.pathname}::__main__"
        formatted = json.dumps(_json_record_dict(record))
        if self.color and _COLOR:
            formatted = "".join(
                (_COLORS[record.levelname[0]], formatted, Fore.WHITE)
            )
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        return formatted


class Lager(logging.Logger):
    def _calling_frame(self, nback=3):
        callerframerecord = inspect.stack()[nback]  # 0 represents this line
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        call_filename = os.path.split(info.filename)[-1]
        call_fn = "{}:{}".format(call_filename, info.function)
        return {"lno": info.lineno, "fn": call_fn}

    def _handle_msg(self, msg):
        if isinstance(msg, str):
            return msg
        if isinstance(msg, dict):
            return json.dumps(msg)

    def _mk_n_handle_record(self, msg, level):
        rec = self.makeRecord(
            name=self.name,
            level=level,
            **self._calling_frame(3),
            msg=msg,
            exc_info=None,
            args=(),
        )
        self.handle(rec)

    def __add__(self, msg):
        self._mk_n_handle_record(msg, logging.INFO)
        return self

    def __iadd__(self, msg):
        self._mk_n_handle_record(msg, logging.INFO)
        return self

    def __sub__(self, msg):
        self._mk_n_handle_record(msg, logging.DEBUG)
        return self

    def __isub__(self, msg):
        self._mk_n_handle_record(msg, logging.DEBUG)
        return self

    def __mul__(self, msg):
        self._mk_n_handle_record(msg, logging.WARNING)
        return self

    def __imul__(self, msg):
        self._mk_n_handle_record(msg, logging.WARNING)
        return self

    def __pow__(self, msg, mod=None):
        self._mk_n_handle_record(msg, logging.ERROR)
        return self

    def __ipow__(self, msg, mod=None):
        self._mk_n_handle_record(msg, logging.ERROR)
        return self

    def d(self, msg):
        self._mk_n_handle_record(msg, logging.DEBUG)

    def i(self, msg):
        self._mk_n_handle_record(msg, logging.INFO)

    def w(self, msg):
        self._mk_n_handle_record(msg, logging.WARNING)

    def e(self, msg):
        self._mk_n_handle_record(msg, logging.ERROR)

    def c(self, msg):
        self._mk_n_handle_record(msg, logging.CRITICAL)


# Register the Lager object
setLoggerClass(Lager)


def _remove_handlers(logger):
    for h in logger.handlers:
        if hasattr(h, _IS_LAGER):
            logger.removeHandler(h)


def all_loggers():
    return {name: getLogger(name) for name in root.manager.loggerDict}


def pour_lager(
    name=None,
    filepath=None,
    level=DEBUG,
    stderr=True,
    tornado=False,
    max_bytes=None,
    logfile_mode="a",
    propagate=False,
):
    """Return a lager-logger"""
    if name is None:
        frame = stack()[1]
        module = getmodule(frame[0])
        name = module.__name__

    if isinstance(level, str):
        try:
            level = _LOG_LEVELS[level.lower()]
        except KeyError:
            log_level_strings = ", ".join(_LOG_LEVELS.keys())
            raise ValueError(
                "Valid string log levels are: {}".format(log_level_strings)
            )
    elif level not in _LOG_LEVELS.values():
        raise ValueError("Not a valid log_level")

    _name = name or __name__
    _lager = getLogger(_name)
    for h in _lager.handlers:
        # print(h)
        if hasattr(h, _IS_LAGER):
            _lager.removeHandler(h)
            continue
        h.setLevel(level)

    if stderr:
        c_handler = StreamHandler()
        setattr(c_handler, _IS_LAGER, True)
        c_handler.setLevel(level)
        c_handler.setFormatter(
            LagerFormatter(
                color=_COLOR and _stderr_colorable(), tornado=tornado
            )
        )
        _lager.addHandler(c_handler)
    if filepath:
        _lager_formatter = LagerFormatter(color=False)
        if max_bytes:
            f_handler = handlers.RotatingFileHandler(
                filepath, maxBytes=max_bytes
            )
        else:
            f_handler = FileHandler(filepath, mode=logfile_mode)
        setattr(f_handler, _IS_LAGER, True)
        f_handler.setLevel(level)
        f_handler.setFormatter(_lager_formatter)
        _lager.addHandler(f_handler)
    _lager.propagate = propagate
    _lager.setLevel(level)
    return _lager


def find_lager(name="lager"):
    """Find the logger with the given name"""
    _all_loggers = all_loggers()
    if name in _all_loggers:
        return _all_loggers[name]
    return pour_lager(name=name)


def find_mod_lager():
    """Find the logger with the given name"""
    frame = stack()[1]
    module = getmodule(frame[0])
    name = module.__name__
    return find_lager(name)


if __name__ == "__main__":
    pass
    # from doctest import testmod
    # testmod()
