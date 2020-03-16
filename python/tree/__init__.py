#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division, print_function

from pkg_resources import parse_version
import os

import yaml

from tree.tree import Tree

# Inits the logging system. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(name).
from .misc import log


NAME = 'tree'

# Loads config
yaml_version = parse_version(yaml.__version__)
with open(os.path.dirname(__file__) + '/etc/{0}.cfg'.format(NAME)) as ff:
    if yaml_version >= parse_version('5.1'):
        config = yaml.load(ff, Loader=yaml.FullLoader)
    else:
        config = yaml.load(ff)


__version__ = '2.15.9dev'
