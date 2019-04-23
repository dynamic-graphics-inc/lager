#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_lager
----------------------------------

Tests for `lager` module.
"""

from lager import pour_lager

def test_write_to_logfile():
    """
    Should log to a file.
    """
    temp_file = 'sometempfile.log'
    logger = pour_lager(logfile=temp_file)
    logger.info('yeah yeah yeah')
