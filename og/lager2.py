# -*- coding: utf-8 -*-
"""
"""
import functools
import inspect
import logging
import os
import sys
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARN
from logging import WARNING
from logging.handlers import RotatingFileHandler
from logging.handlers import SysLogHandler

unicode_type = str
basestring_type = str

import curses  # type: ignore

HAS_COLOR = False
if os.name == "nt":
    from colorama import init as colorama_init

    colorama_init()
    HAS_COLOR = True
else:
    if curses and hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                HAS_COLOR = True

        except Exception:
            pass

_TO_UNICODE_TYPES = (unicode_type, type(None))
DEFAULT_LAGER = "lager_default"
global logger
logger = None
_loglevel = logging.DEBUG
_logfile = None
_formatter = None
_handlers = None

# Colors...
# Source: https://github.com/tartley/colorama/blob/master/colorama/ansi.py
# Copyright: Jonathan Hartley 2013. BSD 3-Clause license.
CSI = "\033["
OSC = "\033]"

def code_to_chars(code):
    return CSI + str(code) + "m"

# def set_title(title):
#     return OSC + "2;" + title + BEL

def clear_screen(mode=2):
    return CSI + str(mode) + "J"

def clear_line(mode=2):
    return CSI + str(mode) + "K"

class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))

class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + "A"

    def DOWN(self, n=1):
        return CSI + str(n) + "B"

    def FORWARD(self, n=1):
        return CSI + str(n) + "C"

    def BACK(self, n=1):
        return CSI + str(n) + "D"

    def POS(self, x=1, y=1):
        return CSI + str(y) + ";" + str(x) + "H"

class AnsiFore(AnsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97

class AnsiBack(AnsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107

class AnsiStyle(AnsiCodes):
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0

ForegroundColors = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()

class Lager(logging.GetLoggerClass()):
    def __init__(
        self, name,
        level=INFO
        ):
        # Initial construct.
        super().__init__(name=name)
        # global _formatter
        # self.format = format
        self.level = level
        self.name = name
        # self.console_formatter = LagerFmt()
        # self.format =
        # "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s"
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(LagerFmt)
        self.format = self.console_logger.format
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_logger)
        self.handlers = self.logger.handlers

    # def info(self, msg, extra=None):
    #     self.logger.info(msg, extra=extra)
    #
    # def error(self, msg, extra=None):
    #     self.logger.error(msg, extra=extra)
    #
    # def debug(self, msg, extra=None):
    #     self.logger.debug(msg, extra=extra)
    #
    # def warn(self, msg, extra=None):
    #     self.logger.warning(msg, extra=extra)

    # def __add__(self, msg):
    #     callerframerecord = inspect.stack()[1]  # 0 represents this line
    #     frame = callerframerecord[0]
    #     info = inspect.getframeinfo(frame)
    #     call_filename = os.path.split(info.filename)[-1]
    #     call_fn = "{}:{}".format(call_filename, info.function)
    #     rec = self.makeRecord(name=self.name,
    #                           level=logging.INFO,
    #                           lno=info.lineno,
    #                           fn=call_fn,
    #                           msg=msg,
    #                           exc_info=(), args=None)
    #     self.logger.handle(rec)
    #     # self.info(msg)
    #     return self

def init_lager(
    name=None,
    log_filepath=None,
    level=logging.DEBUG,
    formatter=None,
    maxBytes=0,
    backupCount=0,
    fileLoglevel=None,
    disableStderrLogger=False,
    ):
    """
    Returns a configured logger or the specified one if the name param exists.
    """
    _logger = Lager(name or __name__)
    _logger.propagate = False
    _logger.setLevel(level)

    # Reconfigure existing handlers
    stderr_stream_handler = None
    for handler in list(_logger.handlers):
        stderr_stream_handler = handler
        handler.setLevel(level)
        handler.setFormatter(formatter or LagerFmt())

    # remove the stderr handler (stream_handler) if disabled
    if disableStderrLogger and stderr_stream_handler is not None:
        _logger.removeHandler(stderr_stream_handler)
    elif stderr_stream_handler is None:
        stderr_stream_handler = logging.StreamHandler()
        setattr(stderr_stream_handler, True)
        stderr_stream_handler.setLevel(level)
        stderr_stream_handler.setFormatter(formatter or LagerFmt())
        _logger.addHandler(stderr_stream_handler)

    if log_filepath:
        rotating_filehandler = RotatingFileHandler(
            filename=log_filepath, maxBytes=maxBytes, backupCount=backupCount
            )
        setattr(rotating_filehandler, True)
        rotating_filehandler.setLevel(fileLoglevel or level)
        rotating_filehandler.setFormatter(formatter or LagerFmt(color=False))
        _logger.addHandler(rotating_filehandler)

    return _logger

class LagerFmt(logging.Formatter):
    """
    Log formatter used in Tornado. Key features of this formatter are:
    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """

    DEFAULT_FORMAT = "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s"
    DEFAULT_DATE_FORMAT = "%y%m%d %H:%M:%S"
    DEFAULT_COLORS = {
        logging.DEBUG  : ForegroundColors.CYAN,
        logging.INFO   : ForegroundColors.GREEN,
        logging.WARNING: ForegroundColors.YELLOW,
        logging.ERROR  : ForegroundColors.RED,
        }

    def __init__(
        self,
        color=True,
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
        colors=DEFAULT_COLORS,
        ):
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt
        self._colors = {}
        self._normal = ""

        if color and HAS_COLOR:
            self._colors = colors
            self._normal = ForegroundColors.RESET

    def format(self, record):
        try:
            message = record.getMessage()
            assert isinstance(message, basestring_type)
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ""

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(_safe_unicode(ln) for ln in record.exc_text.split("\n"))
            formatted = "\n".join(lines)
        return formatted.replace("\n", "\n    ")

_TO_UNICODE_TYPES = (unicode_type, type(None))

def to_unicode(value):
    """
    Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")

def _safe_unicode(s):
    try:
        return to_unicode(s)
    except UnicodeDecodeError:
        return repr(s)

def setup_default_logger(
    logfile=None,
    level=logging.DEBUG,
    formatter=None,
    maxBytes=0,
    backupCount=0,
    disableStderrLogger=False,
    ):
    global logger
    logger = init_lager(
        name=DEFAULT_LAGER,
        log_filepath=logfile,
        level=level,
        formatter=_formatter,
        disableStderrLogger=disableStderrLogger,
        )
    return logger

def reset_lager():
    """
    Resets the internal default logger to the initial configuration
    """
    global logger
    global _loglevel
    global _logfile
    global _formatter
    _loglevel = logging.DEBUG
    _logfile = None
    _formatter = None
    logger = init_lager(
        name=DEFAULT_LAGER, log_filepath=_logfile, level=_loglevel, formatter=_formatter
        )

def lager_abv(level=logging.DEBUG, update_custom_handlers=False):
    logger.setLevel(level)
    for handler in list(logger.handlers):
        handler.setLevel(level)
    global _loglevel
    _loglevel = level

def formatter(formatter, update_custom_handlers=False):
    for handler in list(logger.handlers):
        if hasattr(handler) or update_custom_handlers:
            handler.setFormatter(formatter)
    global _formatter
    _formatter = formatter

def log2file(
    filename,
    formatter=None,
    mode="a",
    maxBytes=0,
    backupCount=0,
    encoding=None,
    loglevel=None,
    disableStderrLogger=False,
    ):
    if filename:
        rotating_filehandler = RotatingFileHandler(
            filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            )
        setattr(rotating_filehandler, True)
        if loglevel:
            setattr(rotating_filehandler, True)

        # Configure the handler and add it to the logger
        rotating_filehandler.setLevel(loglevel or _loglevel)
        rotating_filehandler.setFormatter(
            formatter or _formatter or LagerFmt(color=False)
            )
        logger.addHandler(rotating_filehandler)

def rm_lager_handlers(logger_to_update, disableStderrLogger=True):
    for handler in list(logger_to_update.handlers):
        if hasattr(handler):
            if isinstance(handler, RotatingFileHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, SysLogHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, logging.StreamHandler) and disableStderrLogger:
                logger_to_update.removeHandler(handler)

# Initially setup the default logger
logging.setLoggerClass(Lager)
logger = init_lager(
    name=DEFAULT_LAGER,
    log_filepath=None,
    level=DEBUG,
    formatter=formatter,
    disableStderrLogger=False,
    )

if __name__ == "__main__":
    _logger = init_lager()
    _logger.info("hello")
