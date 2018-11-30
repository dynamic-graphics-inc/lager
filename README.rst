========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-lager/badge/?style=flat
    :target: https://readthedocs.org/projects/python-lager
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/jessekrubin/python-lager.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jessekrubin/python-lager

.. |codecov| image:: https://codecov.io/github/jessekrubin/python-lager/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jessekrubin/python-lager

.. |version| image:: https://img.shields.io/pypi/v/lager.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/lager

.. |commits-since| image:: https://img.shields.io/github/commits-since/jessekrubin/python-lager/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jessekrubin/python-lager/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/lager.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/lager

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lager.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/lager

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lager.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/lager


.. end-badges

python logger on tap

* Free software: MIT license

Installation
============

::

    pip install lager

Documentation
=============


https://python-lager.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
