# encoding: utf-8
#
# setup.py
#


import shutil
from setuptools import setup

# Copy data files into the python/tree/data directory
tmp = shutil.copytree('data', 'python/tree/data', dirs_exist_ok=True)


setup()
