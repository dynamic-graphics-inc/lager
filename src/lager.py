# -*- coding: utf-8 -*-
"""
"""
import functools
import os
import sys
import inspect
import logging
from logging import INFO, ERROR, DEBUG, WARN, WARNING
from logging.handlers import RotatingFileHandler, SysLogHandler

__author__ = """Chris Hager"""
__email__ = 'jessekrubin@gmail.com'
__version__ = '0.1.0'

try:
    import curses  # type: ignore
except ImportError:
    curses = None

if os.name == 'nt':
    from colorama import init as colorama_init

    colorama_init()

# Python 2+3 compatibility settings for logger
bytes_type = bytes
if sys.version_info >= (3,):
    unicode_type = str
    basestring_type = str
    xrange = range
else:
    # The names unicode and basestring don't exist in py3 so silence flake8.
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa

# Name of the internal default logger
LOGZERO_DEFAULT_LOGGER = "lager_default"

# Attribute which all internal loggers carry
LOGZERO_INTERNAL_LOGGER_ATTR = "_is_lager_internal"

# Attribute signalling whether the handler has a custom loglevel
LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL = "_is_lager_internal_handler_custom_loglevel"

# Logzero default logger
global logger
logger = None
# Current state of the internal logging settings
_loglevel = logging.DEBUG
_logfile = None
_formatter = None
_handlers = None

# Colors...
# Source: https://github.com/tartley/colorama/blob/master/colorama/ansi.py
# Copyright: Jonathan Hartley 2013. BSD 3-Clause license.
CSI = '\033['
OSC = '\033]'
BEL = '\007'


def code_to_chars(code):
    return CSI + str(code) + 'm'


def set_title(title):
    return OSC + '2;' + title + BEL


def clear_screen(mode=2):
    return CSI + str(mode) + 'J'


def clear_line(mode=2):
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + 'A'

    def DOWN(self, n=1):
        return CSI + str(n) + 'B'

    def FORWARD(self, n=1):
        return CSI + str(n) + 'C'

    def BACK(self, n=1):
        return CSI + str(n) + 'D'

    def POS(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


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


# Setup colorama on Windows




class Lager(logging.getLoggerClass()):
# class Lager(logging.Logger):
    def __init__(self, name, format="%(asctime)s | %(levelname)s | %(message)s", level=INFO):
        # Initial construct.
        super().__init__(name=name)
        self.format = format
        self.level = level
        self.name = name

        # Logger configuration.
        self.console_formatter = logging.Formatter(self.format)
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(self.console_formatter)

        # Complete logging config.
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_logger)
        self.handlers = self.logger.handlers

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)

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


    # def __add__(self, msg):
    #     try:
    #         return self.__iadd__(msg)
    #     except UnboundLocalError:
    #         pass
    #     finally:
    #         return self

    # def __sub__(self, msg):
    #     Lager.log(self.log_ops['-'], msg)
    #     return self
    #
    # def __mul__(self, msg):
    #     Lager.log(self.log_ops['*'], msg)
    #     return self
    #
    # def __pow__(self, msg, modulo=None):
    #     Lager.log(self.log_ops['**'], msg)
    #     return self
    #
    # def __mod__(self, msg):
    #     Lager.log(self.log_ops['%'], msg)
    #     return self
    #
    # def __iadd__(self, msg):
    #     return self.__add__('{} __NO_CONSOLE__'.format(msg))
    #
    # def __isub__(self, msg):
    #     return self.__sub__('{} __NO_CONSOLE__'.format(msg))
    #
    # def __imul__(self, msg):
    #     return self.__mul__('{} __NO_CONSOLE__'.format(msg))
    #
    # def __ipow__(self, msg):
    #     return self.__pow__('{} __NO_CONSOLE__'.format(msg))
    #
    # def __imod__(self, msg):
    #     return self.__mod__('{} __NO_CONSOLE__'.format(msg))



def setup_logger(name=None,
                 filpath=None,
                 level=logging.DEBUG,
                 formatter=None, maxBytes=0, backupCount=0,
                 fileLoglevel=None, disableStderrLogger=False):
    """
    Configures and returns a fully configured logger instance, no hassles.
    If a logger with the specified name already exists, it returns the existing instance,
    else creates a new one.

    If you set the ``logfile`` parameter with a filename, the logger will save the messages to the logfile,
    but does not rotate by default. If you want to enable log rotation, set both ``maxBytes`` and ``backupCount``.

    Usage:

    .. code-block:: python

        from lager import setup_logger
        logger = setup_logger()
        logger.info("hello")

    :arg string name: Name of the `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_. Multiple calls to ``setup_logger()`` with the same name will always return a reference to the same Logger object. (default: ``__name__``)
    :arg string filpath: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: ``logging.DEBUG``).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg int fileLoglevel: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ for the file logger (is not set, it will use the loglevel from the ``level`` argument)
    :arg bool disableStderrLogger: Should the default stderr logger be disabled. Defaults to False.
    :return: A fully configured Python logging `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_ you can use with ``.debug("msg")``, etc.
    """
    _logger = Lager(name or __name__)
    _logger.propagate = False
    _logger.setLevel(level)

    # Reconfigure existing handlers
    stderr_stream_handler = None
    for handler in list(_logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR):
            if isinstance(handler, logging.FileHandler):
                # Internal FileHandler needs to be removed and re-setup to be able
                # to set a new logfile.
                _logger.removeHandler(handler)
                continue
            elif isinstance(handler, logging.StreamHandler):
                stderr_stream_handler = handler

        # reconfigure handler
        handler.setLevel(level)
        handler.setFormatter(formatter or LogFormatter())

    # remove the stderr handler (stream_handler) if disabled
    if disableStderrLogger:
        if stderr_stream_handler is not None:
            _logger.removeHandler(stderr_stream_handler)
    elif stderr_stream_handler is None:
        stderr_stream_handler = logging.StreamHandler()
        setattr(stderr_stream_handler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
        stderr_stream_handler.setLevel(level)
        stderr_stream_handler.setFormatter(formatter or LogFormatter())
        _logger.addHandler(stderr_stream_handler)

    if filpath:
        rotating_filehandler = RotatingFileHandler(filename=filpath, maxBytes=maxBytes, backupCount=backupCount)
        setattr(rotating_filehandler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
        rotating_filehandler.setLevel(fileLoglevel or level)
        rotating_filehandler.setFormatter(formatter or LogFormatter(color=False))
        _logger.addHandler(rotating_filehandler)

    return _logger


#
# def calling_func_name():
#     return call_frame().f_code.co_name
#
#
# def call_frame():
#     f = sys._getframe()
#     while True:
#         if is_user_source_file(f.f_code.co_filename):
#             return f
#         f = f.f_back
#
#
# def is_user_source_file(filename):
#     return os.path.normcase(filename) not in (_srcfile, logging._srcfile)
#
#
# def _current_source_file():
#     if __file__[-4:].lower() in ['.pyc', '.pyo']:
#         return __file__[:-4] + '.py'
#     else:
#         return __file__


# _srcfile = os.path.normcase(_current_source_file())


class LogFormatter(logging.Formatter):
    """
    Log formatter used in Tornado. Key features of this formatter are:
    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y%m%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG  : ForegroundColors.CYAN,
        logging.INFO   : ForegroundColors.GREEN,
        logging.WARNING: ForegroundColors.YELLOW,
        logging.ERROR  : ForegroundColors.RED
        }

    def __init__(self,
                 color=True,
                 fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT,
                 colors=DEFAULT_COLORS):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        .. versionchanged:: 3.2
           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)

        self._fmt = fmt
        self._colors = {}
        self._normal = ''

        if color and _stderr_supports_color():
            self._colors = colors
            self._normal = ForegroundColors.RESET

    def format(self, record):
        try:
            message = record.getMessage()
            assert isinstance(message,
                              basestring_type)  # guaranteed by logging
            # Encoding notes:  The logging module prefers to work with character
            # strings, but only enforces that log messages are instances of
            # basestring.  In python 2, non-ascii bytestrings will make
            # their way through the logging framework until they blow up with
            # an unhelpful decoding error (with this formatter it happens
            # when we attach the prefix, but there are other opportunities for
            # exceptions further along in the framework).
            #
            # If a byte string makes it this far, convert it to unicode to
            # ensure it will make it out to the logs.  Use repr() as a fallback
            # to ensure that all byte strings can be converted successfully,
            # but don't do it by default so we don't add extra quotes to ascii
            # bytestrings.  This is a bit of a hacky place to do this, but
            # it's worth it since the encoding errors that would otherwise
            # result are so useless (and tornado is fond of using utf8-encoded
            # byte strings wherever possible).
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to _safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(
                _safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def _stderr_supports_color():
    # Colors can be forced with an env variable
    if os.getenv('LOGZERO_FORCE_COLOR') == '1':
        return True

    # Windows supports colors with colorama
    if os.name == 'nt':
        return True

    # Detect color support of stderr with curses (Linux/macOS)
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                return True

        except Exception:
            pass

    return False


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
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")


def _safe_unicode(s):
    try:
        return to_unicode(s)
    except UnicodeDecodeError:
        return repr(s)


def setup_default_logger(logfile=None, level=logging.DEBUG, formatter=None, maxBytes=0, backupCount=0,
                         disableStderrLogger=False):
    """
    Deprecated. Use `lager.loglevel(..)`, `lager.logfile(..)`, etc.

    Globally reconfigures the default `lager.logger` instance.

    Usage:

    .. code-block:: python

        from lager import logger, setup_default_logger
        setup_default_logger(level=logging.WARN)
        logger.info("hello")  # this will not be displayed anymore because minimum loglevel was set to WARN

    :arg string logfile: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `logging.DEBUG`).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg bool disableStderrLogger: Should the default stderr logger be disabled. Defaults to False.
    """
    global logger
    logger = setup_logger(name=LOGZERO_DEFAULT_LOGGER, filpath=logfile, level=level, formatter=formatter,
                          disableStderrLogger=disableStderrLogger)
    print("in setup")
    return logger


def reset_default_logger():
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
    logger = setup_logger(name=LOGZERO_DEFAULT_LOGGER,
                          filpath=_logfile,
                          level=_loglevel, formatter=_formatter)


def loglevel(level=logging.DEBUG, update_custom_handlers=False):
    """
    Set the minimum loglevel for the default logger (`lager.logger`).

    This reconfigures only the internal handlers of the default logger (eg. stream and logfile).
    You can also update the loglevel for custom handlers by using `update_custom_handlers=True`.

    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `logging.DEBUG`).
    :arg bool update_custom_handlers: If you added custom handlers to this logger and want this to update them too, you need to set `update_custom_handlers` to `True`
    """
    logger.setLevel(level)

    # Reconfigure existing internal handlers
    for handler in list(logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR) or update_custom_handlers:
            # Don't update the loglevel if this handler uses a custom one
            if hasattr(handler, LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL):
                continue

            # Update the loglevel for all default handlers
            handler.setLevel(level)

    global _loglevel
    _loglevel = level


def formatter(formatter, update_custom_handlers=False):
    """
    Set the formatter for all handlers of the default logger (``lager.logger``).

    This reconfigures only the lager internal handlers by default, but you can also
    reconfigure custom handlers by using ``update_custom_handlers=True``.

    Beware that setting a formatter which uses colors also may write the color codes
    to logfiles.

    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg bool update_custom_handlers: If you added custom handlers to this logger and want this to update them too, you need to set ``update_custom_handlers`` to `True`
    """
    for handler in list(logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR) or update_custom_handlers:
            handler.setFormatter(formatter)

    global _formatter
    _formatter = formatter


def logfile(filename, formatter=None, mode='a', maxBytes=0, backupCount=0, encoding=None, loglevel=None,
            disableStderrLogger=False):
    """
    Setup logging to file (using a `RotatingFileHandler <https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`_ internally).

    By default, the file grows indefinitely (no rotation). You can use the ``maxBytes`` and
    ``backupCount`` values to allow the file to rollover at a predetermined size. When the
    size is about to be exceeded, the file is closed and a new file is silently opened
    for output. Rollover occurs whenever the current log file is nearly ``maxBytes`` in length;
    if either of ``maxBytes`` or ``backupCount`` is zero, rollover never occurs.

    If ``backupCount`` is non-zero, the system will save old log files by appending the
    extensions ‘.1’, ‘.2’ etc., to the filename. For example, with a ``backupCount`` of 5
    and a base file name of app.log, you would get app.log, app.log.1, app.log.2, up to
    app.log.5. The file being written to is always app.log. When this file is filled,
    it is closed and renamed to app.log.1, and if files app.log.1, app.log.2, etc. exist,
    then they are renamed to app.log.2, app.log.3 etc. respectively.

    :arg string filename: Filename of the logfile. Set to `None` to disable logging to the logfile.
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg string mode: mode to open the file with. Defaults to ``a``
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg string encoding: Used to open the file with that encoding.
    :arg int loglevel: Set a custom loglevel for the file logger, else uses the current global loglevel.
    :arg bool disableStderrLogger: Should the default stderr logger be disabled. Defaults to False.
    """
    # Step 1: If an internal RotatingFileHandler already exists, remove it
    # __remove_internal_loggers(logger, disableStderrLogger)

    # Step 2: If wanted, add the RotatingFileHandler now
    if filename:
        rotating_filehandler = RotatingFileHandler(filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount,
                                                   encoding=encoding)

        # Set internal attributes on this handler
        setattr(rotating_filehandler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
        if loglevel:
            setattr(rotating_filehandler, LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL, True)

        # Configure the handler and add it to the logger
        rotating_filehandler.setLevel(loglevel or _loglevel)
        rotating_filehandler.setFormatter(formatter or _formatter or LogFormatter(color=False))
        logger.addHandler(rotating_filehandler)


def __remove_internal_loggers(logger_to_update, disableStderrLogger=True):
    """
    Remove the internal loggers (e.g. stderr logger and file logger) from the specific logger
    :param logger_to_update: the logger to remove internal loggers from
    :param disableStderrLogger: should the default stderr logger be disabled? defaults to True
    """
    for handler in list(logger_to_update.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR):
            if isinstance(handler, RotatingFileHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, SysLogHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, logging.StreamHandler) and disableStderrLogger:
                logger_to_update.removeHandler(handler)


def log_function_call(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join(["%s=%s" % (key, kwargs[key]) for key in kwargs])
        if args_str and kwargs_str:
            all_args_str = ", ".join([args_str, kwargs_str])
        else:
            all_args_str = args_str or kwargs_str
        # logger.debug("%s(%s)", func.__name__, all_args_str)
        print("%s(%s)", func.__name__, all_args_str)
        return func(*args, **kwargs)
    return wrap
# Initially setup the default logger
logger = setup_logger()
logging.setLoggerClass(Lager)

if __name__ == "__main__":
    _logger = setup_logger()
    _logger.info("hello")
