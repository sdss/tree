# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2016-10-11 13:24:56
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-11-29 17:56:19

from __future__ import print_function, division, absolute_import
import os
from collections import OrderedDict
from configparser import SafeConfigParser


class Tree(object):
    ''' Initialize the sdss tree object

    This class provides Python programmatic access to the SDSS tree envionment structure

    Parameters:
        key (str|list):
            A section or list of sections of the tree to add into the local environment
        uproot_with (str):
            A new TREE_DIR path used to override an existing TREE_DIR environment variable

    Attributes:
        treedir (str):
            The directory of the tree
        environ (dict):
            The fully loaded SDSS config file

    '''

    def __init__(self, *args, **kwargs):
        key = kwargs.get('key', None)
        uproot_with = kwargs.get('uproot_with', None)
        self.setRoots(uproot_with=uproot_with)
        self.loadConfig()
        self.branchOut(limb=key)
        # add the general directories
        if key is not None:
            self.addPathsToOS(key='general')
        self.addPathsToOS(key=key)

    def __repr__(self):
        return ('Tree(sas_base_dir={0})'.format(self.sasbasedir))

    def setRoots(self, uproot_with=None):
        ''' Set the roots of the tree in the os environment

        Parameters:
            uproot_with (str):
                A new TREE_DIR path used to override an existing TREE_DIR environment variable

        '''

        # Check for TREE_DIR
        self.treedir = os.environ.get('TREE_DIR', None) if not uproot_with else uproot_with
        if not self.treedir:
            treefilepath = os.path.dirname(os.path.abspath(__file__))
            if 'python/' in treefilepath:
                self.treedir = treefilepath.rsplit('/', 2)[0]
            else:
                self.treedir = treefilepath
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
        ''' loads the sdsswork config file '''

        self._cfg = SafeConfigParser()
        self._cfg.read(self.configfile)
        # create the local tree environment
        self.environ = OrderedDict()
        self.environ['default'] = self._cfg.defaults()
        # set the filesystem envvar to sas_base_dir
        self._file_replace = '@FILESYSTEM@'
        if self.environ['default']['filesystem'] == self._file_replace:
            self.environ['default']['filesystem'] = self.sasbasedir

    def branchOut(self, limb=None):
        ''' Set the individual section branches

        This adds the various sections of the config file into the
        tree environment for access later. Optically can specify a specific
        branch.

        Parameters:
            branch (str/list):
                The name of the section of the config to add into the environ
                or a list of strings

        '''

        # Filter on sections
        if not limb:
            limbs = self._cfg.sections()
        else:
            # we must have the general always + secton
            limb = limb if isinstance(limb, list) else [limb]
            limbs = ['general']
            limbs.extend(limb)

        # add all limbs into the tree environ
        for leaf in limbs:
            leaf = leaf if leaf in self._cfg.sections() else leaf.upper()
            self.environ[leaf] = OrderedDict()
            options = self._cfg.options(leaf)

            for opt in options:
                if opt in self.environ['default']:
                    continue
                val = self._cfg.get(leaf, opt)
                if val.find(self._file_replace) == 0:
                    val = val.replace(self._file_replace, self.sasbasedir)
                self.environ[leaf][opt] = val

    def getPaths(self, key):
        ''' Retrieve a set of environment paths from the config

        Parameters:
            key (str):
                The section name to grab from the environment

        Returns:
            self.environ[newkey] (OrderedDict):
                An ordered dict containing all of the paths from the
                specified section, as key:val = name:path
        '''
        newkey = key if key in self.environ else key.upper() if key.upper() \
            in self.environ else None
        if newkey:
            return self.environ[newkey]
        else:
            raise KeyError('Key {0} not found in tree environment'.format(key))

    def addPathsToOS(self, key=None):
        ''' Add the paths in tree environ into the os environ

        This code goes through the tree environ and checks
        for existence in the os environ, then adds them

        Parameters:
            key (str):
                The section name to check against / add
        '''

        if key is not None:
            allpaths = key if isinstance(key, list) else [key]
        else:
            allpaths = [k for k in self.environ.keys() if 'default' not in k]

        for key in allpaths:
            paths = self.getPaths(key)
            self.checkPaths(paths)

    def checkPaths(self, paths):
        ''' Check if the path is in the os environ, and if not add it

        Paramters:
            paths (OrderedDict):
                An ordered dict containing all of the paths from the
                a given section, as key:val = name:path
        '''
        for pathname, path in paths.items():
            if pathname.upper() not in os.environ:
                os.environ[pathname.upper()] = os.path.normpath(path)


