# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2016-10-11 13:24:56
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-06-30 14:01:05

from __future__ import absolute_import, division, print_function

import os
import sys
from collections import OrderedDict

import six


if ((sys.version_info.major == 3 and sys.version_info.minor > 2) or
        (sys.version_info.major == 2 and sys.version_info.minor >= 7)):
    from configparser import ConfigParser as SafeConfigParser
else:
    from configparser import SafeConfigParser


class Tree(object):
    ''' Initialize the sdss tree object

    This class provides Python programmatic access to the SDSS tree envionment structure

    Parameters:
        key (str|list):
            A section or list of sections of the tree to add into the local environment
        uproot_with (str):
            A new TREE_DIR path used to override an existing TREE_DIR environment variable
        config (str):
            Name of manual config file to load.  Default is sdsswork.
        update (bool):
            If True, overwrites existing tree environment variables in your
            local environment.  Default is False.
        exclude (list):
            A list of environment variables to exclude
            from forced updates

    Attributes:
        treedir (str):
            The directory of the tree
        environ (dict):
            The fully loaded SDSS config file held internally

    '''

    def __init__(self, *args, **kwargs):
        self.key = kwargs.get('key', None)
        uproot_with = kwargs.get('uproot_with', None)
        update = kwargs.get('update', False)
        self.exclude = kwargs.get('exclude', [])
        self.config_name = kwargs.get('config', 'sdsswork')
        self.set_roots(uproot_with=uproot_with)
        self.load_config()
        self.branch_out(limb=self.key)
        # add the general directories
        if self.key is not None:
            self.add_paths_to_os(key='general', update=update)
        self.add_paths_to_os(key=self.key, update=update)

    def __repr__(self):
        return ('Tree(sas_base_dir={0}, config={1})'.format(self.sasbasedir, self.config_name))

    def list_keys(self):
        ''' List the available keys you can load '''
        return [k for k in self.environ.keys() if k not in ['general', 'default']]

    def set_roots(self, uproot_with=None):
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
            self.treedir = treefilepath
            os.environ['TREE_DIR'] = self.treedir

        # Check sas_base_dir
        if 'SAS_BASE_DIR' in os.environ:
            self.sasbasedir = os.environ["SAS_BASE_DIR"]
        else:
            self.sasbasedir = os.path.expanduser('~/sas')

        # make the directories
        if not os.path.isdir(self.sasbasedir):
            os.makedirs(self.sasbasedir)

    def load_config(self, config=None):
        ''' loads a config file

        Parameters:
            config (str):
                Optional name of manual config file to load
        '''

        # Read the config file
        cfgname = (config or self.config_name)
        cfgname = 'sdsswork' if cfgname is None else cfgname
        assert isinstance(cfgname, six.string_types), 'config name must be a string'
        config_name = cfgname if cfgname.endswith('.cfg') else '{0}.cfg'.format(cfgname)
        self.configfile = os.path.join(self.treedir, 'data', config_name)

        assert os.path.isfile(self.configfile) is True, 'configfile {0} must exist in the proper directory'.format(self.configfile)

        self._cfg = SafeConfigParser()

        try:
            self._cfg.read(self.configfile.decode('utf-8'))
        except AttributeError:
            self._cfg.read(self.configfile)

        # create the local tree environment
        self.environ = OrderedDict()
        self.environ['default'] = self._cfg.defaults()
        # set the filesystem envvar to sas_base_dir
        self._file_replace = '@FILESYSTEM@'
        if self.environ['default']['filesystem'] == self._file_replace:
            self.environ['default']['filesystem'] = self.sasbasedir

    def branch_out(self, limb=None):
        ''' Set the individual section branches

        This adds the various sections of the config file into the
        tree environment for access later. Optically can specify a specific
        branch.  This does not yet load them into the os environment.

        Parameters:
            limb (str/list):
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

    def add_limbs(self, key=None):
        ''' Add a new section from the tree into the existing os environment

        Parameters:
            key (str):
                The section name to grab from the environment

        '''
        self.branch_out(limb=key)
        self.add_paths_to_os(key=key)

    def get_paths(self, key):
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

    def add_paths_to_os(self, key=None, update=None):
        ''' Add the paths in tree environ into the os environ

        This code goes through the tree environ and checks
        for existence in the os environ, then adds them

        Parameters:
            key (str):
                The section name to check against / add
            update (bool):
                If True, overwrites existing tree environment variables in your
                local environment.  Default is False.
        '''

        if key is not None:
            allpaths = key if isinstance(key, list) else [key]
        else:
            allpaths = [k for k in self.environ.keys() if 'default' not in k]

        for key in allpaths:
            paths = self.get_paths(key)
            self.check_paths(paths, update=update)

    def check_paths(self, paths, update=None):
        ''' Check if the path is in the os environ, and if not add it

        Paramters:
            paths (OrderedDict):
                An ordered dict containing all of the paths from the
                a given section, as key:val = name:path
            update (bool):
                If True, overwrites existing tree environment variables in your
                local environment.  Default is False.
        '''

        # set up the exclusion list
        exclude = [] if not self.exclude else self.exclude \
            if isinstance(self.exclude, list) else [self.exclude]

        # check the path names
        for pathname, path in paths.items():
            if update and pathname.upper() not in exclude:
                os.environ[pathname.upper()] = os.path.normpath(path)
            elif pathname.upper() not in os.environ:
                os.environ[pathname.upper()] = os.path.normpath(path)

    def replant_tree(self, config=None, exclude=None):
        ''' Replant the tree with a different config setup

        Parameters:
            config (str):
                The config name to reload
            exclude (list):
                A list of environment variables to exclude
                from forced updates
        '''

        # reinitialize a new Tree with a new config
        self.__init__(key=self.key, config=config, update=True, exclude=exclude)
