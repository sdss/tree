# encoding: utf-8
#
# setup.py
#


import distutils.dir_util
from setuptools import setup

# Copy data files into the python/tree/data directory
tmp = distutils.dir_util.copy_tree('data', 'python/tree/data')


setup()

