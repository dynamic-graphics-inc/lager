# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
import asyncio
import sys

from functools import wraps
from time import time
from typing import Union

from loguru import logger as lager
from loguru._logger import Logger


__version__ = "0.2.3"

TORNADO_LOGURU_FMT = "<level>[{level.name[0]} {time:YYMMDDTHH:mm:ss} {name}:{module}:{line}]</level> {message}"

lager.t = lager.trace
lager.d = lager.debug
lager.i = lager.info
lager.s = lager.success
lager.w = lager.warning
lager.e = lager.error
lager.c = lager.critical


def loglevel(level: Union[str, int]) -> str:
    log_levels = {
        "notset": "NOTSET",
        "n": "NOTSET",
        "debug": "DEBUG",
        "d": "DEBUG",
        "info": "INFO",
        "i": "INFO",
        "s": "SUCCESS",
        "success": "SUCCESS",
        "warning": "WARNING",
        "warn": "WARNING",
        "w": "WARNING",
        "error": "ERROR",
        "e": "ERROR",
        "critical": "CRITICAL",
        "fatal": "CRITICAL",
        "c": "CRITICAL",
        # enum/enum-strings
        "0": "NOTSET",
        "10": "DEBUG",
        "20": "INFO",
        "25": "SUCCESS",
        "30": "WARNING",
        "40": "ERROR",
        "50": "CRITICAL",
    }
    if isinstance(level, int):
        return loglevel(str(level))
    return log_levels[level.strip('\'').strip('\"').lower()]


def pour_lager(level="d", filepath=None, stderr=True,) -> Logger:
    level = loglevel(level)
    if level != "DEBUG":
        lager.remove()
    if stderr:
        lager.add(sys.stderr, level=level)
    if filepath:
        lager.add(filepath, level=level)
    return lager


def flog(funk=None, level="debug", enter=True, exit=True):
    """Log function (sync/async) enter and exit using this decorator

    Args:
        funk (Callable): Function to decorate
        level (Union[int, str]): Log level
        enter (bool): Log function entry if True
        exit (bool): Log function exit if False

    Returns:
        A wrapped function that now has logging!

    Usage:
        # SYNC
        @flog
        def add(a, b):
            return a + b
        add(1, 4)

        # ASYNC
        @flog
        async def add_async(a, b):
            return a + b
        import asyncio
        asyncio.run(add_async(1, 4))

    """

    def _flog(funk):
        name = funk.__name__

        @wraps(funk)
        def _flog_decorator(*args, **kwargs):
            logger_ = lager.opt(depth=1)
            if enter:
                logger_.log(
                    loglevel(level),
                    "FLOG-ENTER > '{}' (args={}, kwargs={})",
                    name,
                    args,
                    kwargs,
                )
            ti = time()
            result = funk(*args, **kwargs)
            tf = time()
            if exit:
                logger_.log(
                    loglevel(level),
                    "FLOG-EXIT < '{}' (return={}, dt_sec={})",
                    name,
                    result,
                    tf - ti,
                )
            return result

        @wraps(funk)
        async def _flog_decorator_async(*args, **kwargs):
            logger_ = lager.opt(depth=7)
            if enter:
                logger_.log(
                    loglevel(level),
                    "FLOG-ENTER > '{}' (args={}, kwargs={})",
                    name,
                    args,
                    kwargs,
                )
            ti = time()
            result = await funk(*args, **kwargs)
            tf = time()
            if exit:
                logger_.log(
                    loglevel(level),
                    "FLOG-EXIT < '{}' (return={}, dt_sec={})",
                    name,
                    result,
                    tf - ti,
                )
            return result

        if asyncio.iscoroutinefunction(funk) or asyncio.iscoroutine(funk):
            return _flog_decorator_async
        return _flog_decorator

    return _flog(funk) if funk else _flog
