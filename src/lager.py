import logging
from logging import DEBUG, WARN, ERROR, CRITICAL, WARNING
from logging import INFO
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger
from structlog import configure
from structlog import getLogger
from structlog import processors
from structlog import stdlib
from structlog import threadlocal

_LOG_FILE = None
_LOG_LEVELS = {
    'debug'   : DEBUG,
    'd'       : DEBUG,
    'info'    : INFO,
    'i'       : INFO,
    'warning' : WARNING,
    'w'       : WARNING,
    'error'   : ERROR,
    'e'       : ERROR,
    'critical': CRITICAL,
    'c'       : CRITICAL,
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
        stdlib.render_to_log_kwargs]
    )

def pour_lager(
    name=None,
    logfile=None,
    level=DEBUG,
    log2stderr=True,
    maxBytes=None,
    logfile_level=None,
    logfile_mode='a'
    ):
    if isinstance(level, str):
        try:
            level = _LOG_LEVELS[level.lower()]
        except KeyError as e:
            log_level_strings = ', '.join(_LOG_LEVELS.keys())
            raise ValueError(
                'Valid string log levels are: {}'.format(log_level_strings)
                )
    elif level not in _LOG_LEVELS.values():
        raise ValueError('Not a valid log_level')
    _logger = getLogger(name or __name__)
    _json_formatter = jsonlogger.JsonFormatter(
        '(message) (timestamp) (level) (name) (pathname) (lineno)'
        )
    if log2stderr:
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(_json_formatter)
        _logger.addHandler(c_handler)
    if logfile:
        if maxBytes:
            f_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=maxBytes)
            f_handler.setLevel(logfile_level or level)
            f_handler.setFormatter(_json_formatter)
            _logger.addHandler(f_handler)
        else:
            f_handler = logging.FileHandler(logfile, mode=logfile_mode)
            f_handler.setLevel(logfile_level or level)
            f_handler.setFormatter(_json_formatter)
            _logger.addHandler(f_handler)
    _logger.propagate = True
    _logger.setLevel(INFO)
    return _logger

LOG = pour_lager()

if __name__ == '__main__':
    pass
