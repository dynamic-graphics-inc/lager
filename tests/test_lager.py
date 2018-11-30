#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_lager
----------------------------------

Tests for `lager` module.
"""
import os
import logging

import lager
from lager import logger
import pytest


def test_write_to_logfile():
    """
    Should log to a file.
    """
    lager.reset_default_logger()
    temp = 'sometempfile.log'
    # logger = lager.setup_logger(logfile=temp)
    lager.logfile(temp)
    logger.info("test log output")

    lager.logfile(None)
    with open(temp) as f:
        content = f.read()
        assert " test_lager:" in content
        assert content.endswith("test log output\n")
    os.remove(temp)

def test_level():
    """
    Should not log any debug messages if minimum level is set to INFO
    """
    lager.reset_default_logger()
    temp = 'should_be_empty.log'
    lager.logfile(temp)
    lager.loglevel(logging.INFO)
    logger.debug("test log output")
    lager.logfile(None)
    with open(temp) as f:
        content = f.read().replace(' ', '').replace('\n', '')
        assert len(content) == 0
    os.remove(temp)

def test_bytes():
    """
    Should log to a file.
    """
    lager.reset_default_logger()
    temp = 'bytes.log'
    lager.logfile(temp)
    bytes2log = os.urandom(10)
    logger.info(bytes2log)
    lager.logfile(None)
    with open(temp) as f:
        content = f.read()
    assert str(bytes2log) in content
    os.remove(temp)

#
#
# def test_multiple_loggers_one_logfile():
#     """
#     Should properly log bytes
#     """
#     lager.reset_default_logger()
#     temp = tempfile.NamedTemporaryFile()
#     try:
#         logger1 = lager.setup_logger(name="logger1", logfile=temp.name)
#         logger2 = lager.setup_logger(name="logger2", logfile=temp.name)
#         logger3 = lager.setup_logger(name="logger3", logfile=temp.name)
#
#         logger1.info("logger1")
#         logger2.info("logger2")
#         logger3.info("logger3")
#
#         with open(temp.name) as f:
#             content = f.read().strip()
#             assert "logger1" in content
#             assert "logger2" in content
#             assert "logger3" in content
#             assert len(content.split("\n")) == 3
#
#     finally:
#         temp.close()
#
#
# def test_default_logger(disableStdErrorLogger=False):
#     """
#     Default logger should work and be able to be reconfigured.
#     """
#     lager.reset_default_logger()
#     temp = tempfile.NamedTemporaryFile()
#     try:
#         lager.setup_default_logger(logfile=temp.name, disableStderrLogger=disableStdErrorLogger)
#         lager.logger.debug("debug1")  # will be logged
#
#         # Reconfigure with loglevel INFO
#         lager.setup_default_logger(logfile=temp.name, level=logging.INFO, disableStderrLogger=disableStdErrorLogger)
#         lager.logger.debug("debug2")  # will not be logged
#         lager.logger.info("info1")  # will be logged
#
#         # Reconfigure with a different formatter
#         log_format = '%(color)s[xxx]%(end_color)s %(message)s'
#         formatter = lager.LogFormatter(fmt=log_format)
#         lager.setup_default_logger(logfile=temp.name, level=logging.INFO, formatter=formatter, disableStderrLogger=disableStdErrorLogger)
#
#         lager.logger.info("info2")  # will be logged with new formatter
#         lager.logger.debug("debug3")  # will not be logged
#
#         with open(temp.name) as f:
#             content = f.read()
#             test_default_logger_output(content)
#
#     finally:
#         temp.close()
#
#
# @pytest.mark.skip(reason="not a standalone test")
# def test_default_logger_output(content):
#     assert "] debug1" in content
#     assert "] debug2" not in content
#     assert "] info1" in content
#     assert "xxx] info2" in content
#     assert "] debug3" not in content
#
#
# def test_setup_logger_reconfiguration():
#     """
#     Should be able to reconfigure without loosing custom handlers
#     """
#     lager.reset_default_logger()
#     temp = tempfile.NamedTemporaryFile()
#     temp2 = tempfile.NamedTemporaryFile()
#     try:
#         lager.setup_default_logger(logfile=temp.name)
#
#         # Add a custom file handler
#         filehandler = logging.FileHandler(temp2.name)
#         filehandler.setLevel(logging.DEBUG)
#         filehandler.setFormatter(lager.LogFormatter(color=False))
#         lager.logger.addHandler(filehandler)
#
#         # First debug message goes to both files
#         lager.logger.debug("debug1")
#
#         # Reconfigure logger to remove logfile
#         lager.setup_default_logger()
#         lager.logger.debug("debug2")
#
#         # Reconfigure logger to add logfile
#         lager.setup_default_logger(logfile=temp.name)
#         lager.logger.debug("debug3")
#
#         # Reconfigure logger to set minimum loglevel to INFO
#         lager.setup_default_logger(logfile=temp.name, level=logging.INFO)
#         lager.logger.debug("debug4")
#         lager.logger.info("info1")
#
#         # Reconfigure logger to set minimum loglevel back to DEBUG
#         lager.setup_default_logger(logfile=temp.name, level=logging.DEBUG)
#         lager.logger.debug("debug5")
#
#         with open(temp.name) as f:
#             content = f.read()
#             assert "] debug1" in content
#             assert "] debug2" not in content
#             assert "] debug3" in content
#             assert "] debug4" not in content
#             assert "] info1" in content
#             assert "] debug5" in content
#
#         with open(temp2.name) as f:
#             content = f.read()
#             assert "] debug1" in content
#             assert "] debug2" in content
#             assert "] debug3" in content
#             assert "] debug4" not in content
#             assert "] info1" in content
#             assert "] debug5" in content
#
#     finally:
#         temp.close()
#
#
# def test_setup_logger_logfile_custom_loglevel(capsys):
#     """
#     setup_logger(..) with filelogger and custom loglevel
#     """
#     lager.reset_default_logger()
#     temp = tempfile.NamedTemporaryFile()
#     try:
#         logger = lager.setup_logger(logfile=temp.name, fileLoglevel=logging.WARN)
#         logger.info("info1")
#         logger.warn("warn1")
#
#         with open(temp.name) as f:
#             content = f.read()
#             assert "] info1" not in content
#             assert "] warn1" in content
#
#     finally:
#         temp.close()
#
#
# def test_log_function_call():
#     @lager.log_function_call
#     def example():
#         """example doc"""
#         pass
#
#     assert example.__name__ == "example"
#     assert example.__doc__ == "example doc"
#
