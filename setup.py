# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='lager',
      version='0.0.1',
      description='lager ~ the sweet logging module',
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
      repository='https://github.com/jessekrubin/lager',
      url='https://upload.pypi.org/legacy/',
      author_email='jessekrubin@gmail.com',
      author='jessekrubin',
      license='MIT',
      packages=find_packages(),
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=True
      )

