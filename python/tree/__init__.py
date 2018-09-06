#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division, print_function

import os

import yaml

from tree.tree import Tree

# Inits the logging system. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(name).
from .misc import log


NAME = 'tree'

# Loads config
with open(os.path.dirname(__file__) + '/etc/{0}.cfg'.format(NAME)) as ff:
    config = yaml.load(ff)


__version__ = '2.15.6dev'
