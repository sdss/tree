#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division, print_function
from sdsstools import get_config, get_logger, get_package_version


NAME = 'sdss-tree'


# init the logger
log = get_logger(NAME)


# Loads config
config = get_config('tree')


__version__ = get_package_version(path=__file__, package_name=NAME)


from tree.tree import Tree
