# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2016-10-11 13:24:56
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2016-10-11 21:38:29

from __future__ import print_function, division, absolute_import
import os
from collections import OrderedDict
from ConfigParser import SafeConfigParser


class Tree(object):
    ''' The Tree Class '''

    def __init__(self, *args, **kwargs):
        ''' initialize the sdss tree '''
        key = kwargs.get('key', None)
        self.setRoots()
        self.loadConfig()
        self.setSurveyRoots(section=key)
        self.addPathsToOS(key=key)

    def __repr__(self):
        return ('Tree(sas_base_dir={0})'.format(self.sasbasedir))

    def setRoots(self):
        ''' Set the roots of the tree in the os environment '''

        # Check for TREE_DIR
        self.treedir = os.environ.get('TREE_DIR', None)
        if not self.treedir:
            treefilepath = os.path.dirname(os.path.abspath(__file__))
            self.treedir = treefilepath.rsplit('/', 2)[0]
            os.environ['TREE_DIR'] = self.treedir

        # Read the config file
        self.configfile = os.path.join(self.treedir, 'data', 'sdsswork.cfg')

        # Check sas_base_dir
        if 'SAS_BASE_DIR' in os.environ:
            self.sasbasedir = os.environ["SAS_BASE_DIR"]
        else:
            self.sasbasedir = os.path.expanduser('~/sas')

        # make the directories
        if not os.path.isdir(self.sasbasedir):
            os.makedirs(self.sasbasedir)

    def loadConfig(self):
        ''' load the Config file '''
        self._cfg = SafeConfigParser()
        self._cfg.read(self.configfile)
        self.environ = OrderedDict()
        self.environ['default'] = self._cfg.defaults()
        self._file_replace = '@FILESYSTEM@'
        if self.environ['default']['filesystem'] == self._file_replace:
            self.environ['default']['filesystem'] = self.sasbasedir

    def setSurveyRoots(self, section=None):
        ''' Set the individual survey roots '''

        # filter on section
        if not section:
            sections = self._cfg.sections()
        else:
            sections = ['general', section]

        # add all sections into the tree environ
        for sec in sections:
            self.environ[sec] = OrderedDict()
            options = self._cfg.options(sec)
            for opt in options:
                if opt in self.environ['default']:
                    continue
                val = self._cfg.get(sec, opt)
                if val.find(self._file_replace) == 0:
                    val = val.replace(self._file_replace, self.sasbasedir)
                self.environ[sec][opt] = val

    def getPaths(self, key):
        ''' Retrieve a set of environment paths from the config '''
        newkey = key if key in self.environ else key.upper() if key.upper() \
            in self.environ else None
        if newkey:
            return self.environ[newkey]
        else:
            raise KeyError('Key {0} not found in tree environment'.format(key))

    def addPathsToOS(self, key=None):
        ''' add the paths in tree environment into the os environment '''

        if key is not None:
            paths = self.getPaths(key)
            self.checkPaths(paths)
        else:
            allpaths = [k for k in self.environ.keys() if 'default' not in k]
            for key in allpaths:
                paths = self.getPaths(key)
                self.checkPaths(paths)

    def checkPaths(self, paths):
        ''' check if the path is in the os environ, and if not add it '''
        for pathname, path in paths.items():
            if pathname.upper() not in os.environ:
                os.environ[pathname.upper()] = os.path.normpath(path)


