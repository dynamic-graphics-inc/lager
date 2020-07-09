# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
from lager.const import LAGER_PORT
from lager.const import LOGURU_DEFAULT_FMT
from lager.const import TORNADO_FMT
from lager._version import VERSION_MAJOR
from lager._version import VERSION_MINOR
from lager._version import VERSION_PATCH
from lager._version import VERSION_INFO
from lager._version import __version__
from lager.core import loglevel
from lager.core import flog
from lager.core import LOG
from lager.core import LN
from lager.core import ln
from lager.core import log
from lager.core import handlers


__all__ = [
    'LAGER_PORT',
    'VERSION_MAJOR',
    'VERSION_MINOR',
    'VERSION_PATCH',
    'VERSION_INFO',
    '__version__',
    'LOGURU_DEFAULT_FMT',
    'TORNADO_FMT',
    'loglevel'
    ]
