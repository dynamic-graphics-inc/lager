#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(
    name='lager',
    version='0.3.0',
    description='lager ~ a sweet way to log',
    long_description='coming soon',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
        ],
    keywords='logging',
    url='https://github.com/jessekrubin/lager',
    # url='https://upload.pypi.org/legacy/',
    author_email='jessekrubin@gmail.com',
    author='jessekrubin',
    license='MIT license',
    py_modules=["lager"],
    install_requires=[
        ],
    include_package_data=True,
    zip_safe=False
    )
