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
import glob
import re
from collections import OrderedDict
import six
import json
from tree import log, config as cfg_params

if ((sys.version_info.major == 3 and sys.version_info.minor > 2) or
        (sys.version_info.major == 2 and sys.version_info.minor >= 7)):
    from configparser import ConfigParser as SafeConfigParser
else:
    from configparser import SafeConfigParser

orig_environ = os.environ.copy()


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
        root (str):
            An absolute directory path to override as the software product root
        git (bool):
            If True, looks for SDSS_GIT_ROOT environment variable as product root instead
            of SDSS_SVN_ROOT

    Attributes:
        treedir (str):
            The directory of the tree
        environ (dict):
            The fully loaded SDSS config file held internally

    '''
    # possible software product roots
    _product_roots = ['PRODUCT_ROOT', 'SDSS_GIT_ROOT', 'SDSS_SVN_ROOT', 'SDSS_INSTALL_PRODUCT_ROOT',
                      'SDSS_PRODUCT_ROOT', 'SDSS4_PRODUCT_ROOT']

    def __init__(self, config=None, key=None, uproot_with=None, update=None, exclude=None,
                 product_root=None, git=None):
        self.config_name = config or 'sdsswork'
        self.exclude = exclude or []
        update = update or False
        self._keys = key
        self._file_replace = '@FILESYSTEM@'

        # set the roots
        self.set_roots(uproot_with=uproot_with)

        # load the configuraiton file
        self.load_config()

        # create the environment
        self.branch_out(limb=key)

        # add the paths to the os.environ
        if key is not None:
            self.add_paths_to_os(key='general', update=update)
        self.add_paths_to_os(key=key, update=update)

        # set the software product root, $PRODUCT_ROOT envvar
        self.productroot_dir = None
        self.set_product_root(root=product_root, git=git)

    def __repr__(self):
        return ('Tree(sas_base_dir={0}, config={1})'.format(self.sasbasedir, self.config_name))

    @property
    def phase(self):
        ''' Return the phase of the survey from the loaded "work" environment '''
        phase = self.environ['default'].get('phase', None)
        if phase and phase.isdigit():
            phase = int(phase)
        return phase

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
        self.treedir = get_tree_dir(uproot_with=uproot_with)

        # Check sas_base_dir
        if 'SAS_BASE_DIR' in os.environ:
            self.sasbasedir = os.environ["SAS_BASE_DIR"]
        else:
            self.sasbasedir = os.path.expanduser('~/sas')

        # make the directories
        if not os.path.isdir(self.sasbasedir):
            os.makedirs(self.sasbasedir)

    def _read_config(self, config=None, bases=None):
        ''' Read a config file

        Uses ConfigParser to read in a cfg file.  If a base
        is identified, then recursively reads in all cfg files and builds
        a master config dictionary object

        Parameters:
            config (str):
                Optional name of config file to load
            bases (list):
                A list of parent config files

        Returns:
            A configParser dictionary object
        '''

        # format name and file
        config_name = config if config.endswith('.cfg') else '{0}.cfg'.format(config)
        config_file = os.path.join(self.treedir, 'data', config_name)
        assert os.path.isfile(
            config_file) is True, 'config file {0} must exist in the data directory'.format(config_file)

        # read initial config file
        cfg = SafeConfigParser()
        cfg.optionxform = lambda option: option
        cfg.read(config_file)

        # check for any bases
        bases = bases if bases else []
        bases.insert(0, os.path.join(self.treedir, 'data', config_name))
        hasbase = 'base' in cfg.defaults()

        # read base config file
        if hasbase:
            return self._read_config(cfg.defaults()['base'], bases=bases)
        else:
            # read in the full list of config files
            cfg = SafeConfigParser()
            cfg.optionxform = lambda option: option
            cfg.read(bases)
            # if both eboss and boss, then remove boss
            if 'EBOSS' in cfg.sections() and 'BOSS' in cfg.sections():
                cfg.remove_section('BOSS')
        return cfg

    def _check_config(self, config=None):
        ''' check the config

        checks the config for syntax and existence.  Defaults to sdsswork
        or a DR if it doesn't exist.

        Parameters:
            config (str):
                The name of the config to check

        Returns:
            The (updated) name of the config
        '''

        # check initial argument
        cfgname = (config or self.config_name)
        cfgname = 'sdsswork' if cfgname is None else cfgname
        assert isinstance(cfgname, six.string_types), 'config name must be a string'
        cfgname = cfgname.lower()

        config_name = cfgname if cfgname.endswith('.cfg') else '{0}.cfg'.format(cfgname)

        # default to another config if not available
        file_base = [os.path.basename(f) for f in self._cfg_files]
        if config_name not in file_base:
            if 'dr' in config_name:
                drint = max(map(int, [re.findall(r'\d{1,2}', f)[0] for f in file_base if 'dr' in f]))
                log.warning('{0} not found. Defaulting to dr{1}.cfg'.format(config_name, drint))
                self.config_name = 'dr{0}'.format(drint)
            else:
                log.warning('{0} not found. Defaulting to sdsswork'.format(config_name))
                self.config_name = 'sdsswork'
            config_name = self.config_name + '.cfg'
        return config_name

    def load_config(self, config=None):
        ''' Load a config file

        Parameters:
            config (str):
                Optional name of manual config file to load
        '''

        # get a list of all config files
        self._cfg_files = glob.glob(os.path.join(self.treedir, 'data', '*.cfg'))
        self._cfg_files.sort()

        # check the config file
        config_name = self._check_config(config)

        # set the confifile
        configfile = os.path.join(self.treedir, 'data', config_name)
        assert os.path.isfile(configfile) is True, ('configfile {0} must exist in the '
                                                    'data directory'.format(configfile))
        self.config_file = configfile

        # read the config
        self._cfg = self._read_config(config=self.config_name)

    def _create_environment(self, cfg=None, sections=None):
        ''' create the environment from the config

        Creates a dictionary with environment definitions
        expanded out

        Parameters:
            config (str):
                Optional name of manual config file to load
            sections (list):
                A list of config sections to load

        Returns:
            An ordered dictionary of envvar definitions
        '''

        # pass in a cfg dict or use the one attached
        cfg = cfg or self._cfg

        # create the local tree environment
        environ = OrderedDict()
        environ['default'] = cfg.defaults()

        # set the filesystem envvar to sas_base_dir
        filesystem = 'FILESYSTEM' if 'FILESYSTEM' in environ[
            'default'] else 'filesystem' if 'filesystem' in environ['default'] else None
        if environ['default'][filesystem] == self._file_replace:
            environ['default'][filesystem] = self.sasbasedir

        # add all sections into the tree environ
        sections = sections if sections else cfg.sections()
        for section in sections:
            # skip if PATHS
            if section == 'PATHS':
                continue

            section = section if section in cfg.sections() else section.upper()
            environ[section] = OrderedDict()
            options = cfg.options(section)

            for opt in options:
                if opt in environ['default']:
                    continue
                val = cfg.get(section, opt)
                if val.find(self._file_replace) == 0:
                    val = val.replace(self._file_replace, self.sasbasedir)
                environ[section][opt] = val

        return environ

    def _create_paths(self, cfg=None):
        ''' create a dictionary of path definitions

        Extracts the PATHS section from a ConfigParser object
        and builds a dictionary of paths for sdss_access

        Parameters:
            cfg (object):
                A configParser object
        Returns:
            An ordered dictionary of sdss_access path definitions
        '''

        # pass in a cfg dict or use the one attached
        cfg = cfg or self._cfg

        # return if no PATHS found
        if not cfg.has_section('PATHS'):
            return None

        paths = OrderedDict()
        for opt in cfg.options('PATHS'):
            if opt in cfg.defaults():
                continue
            paths[opt] = cfg.get('PATHS', opt)

        # sort the paths by name
        paths = OrderedDict({k: paths[k] for k in sorted(paths.keys())})
        return paths

    def branch_out(self, limb=None):
        ''' Set the individual section branches

        This adds the various sections of the config file into the
        tree environment for access later. Optionally can specify a specific
        branch.  This does not yet load them into the os environment.

        Parameters:
            limb (str|list):
                A section or lists of sections of the config to add into the environ

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
        self.environ = self._create_environment(sections=limbs)

        # add all paths into the tree paths dictionary
        self.paths = self._create_paths()

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
            self._check_paths(paths, update=update)

    def _check_paths(self, paths, update=None):
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
        config = 'sdsswork' if not config else config
        self.__init__(key=self._keys, config=config, update=True, exclude=exclude)

    def list_configs(self):
        ''' List available configs to load '''

        files = [os.path.basename(f) for f in self._cfg_files if 'basework.cfg' not in f]
        return files

    def show_forest(self, config=None):
        ''' Show the environment for a specified config

        Creates a dictionary environment for each config in the list of
        available configurations.

        Parameters:
            config (str):
                The config to show

        Returns:
            A dictionary of config environment(s)
        '''

        configs = [config] if config else self.list_configs()
        cfgs = {}
        for cfg in configs:
            cfg_name = cfg.split('.cfg')[0]
            cfg = self._read_config(cfg_name)
            cfgs[cfg_name] = self._create_environment(cfg)

        if len(configs) == 1:
            return cfgs[cfg_name]
        return cfgs

    @staticmethod
    def list_available_configs():
        ''' List the available config files able to be loaded '''

        # get tree dir
        treedir = get_tree_dir()

        # look up the config files from the data directory
        data_path = os.path.join(treedir, 'data')
        cfgs = [i for i in os.listdir(data_path) if i.endswith('.cfg')]
        cfgs.sort()

        # sort the DR subset of config files
        drsort = sorted([i for i in cfgs if 'dr' in i],
                        key=lambda t: int(re.findall('dr(.*?).cfg', t)[0]))
        rest = [[i] for i in cfgs if 'dr' not in i]
        rest.insert(1, drsort)
        sorted_cfgs = sum(rest, [])
        return sorted_cfgs

    @classmethod
    def get_available_releases(cls, public=None):
        ''' Get the available releases

        Parameters:
            public (bool):
                If True, only return public data releases
        '''

        # get the configs
        cfgs = cls.list_available_configs()

        # parse the data releases
        releases = []
        for i in cfgs:
            if public and not i.startswith('dr'):
                continue

            b = i.split('.cfg', 1)[0]
            if 'dr' in b or 'mpl' in b:
                # uppercase any DR or MPLs
                releases.append(b.upper())
            elif 'work' in b and 'WORK' not in releases:
                # reduce alll xxxxwork cfgs to a single "work" release
                releases.append('WORK')
        return releases

    @staticmethod
    def reset_os_environ():
        ''' Resets os.environ with the orignal cache before tree mods '''
        os.environ = orig_environ

    @staticmethod
    def get_orig_os_environ():
        ''' Returns the original os.environ '''
        return orig_environ

    def to_dict(self, collapse=True):
        ''' Convert tree environment to standard dicts

        Converts the nested ``tree.environ`` into a series of
        ordinary dicts.

        Parameters:
            collapse (bool):
                If True, collapses nested dicts into a single dict.  Default is True.
        '''
        if collapse is False:
            dd = json.loads(json.dumps(self.environ))
            dd.pop('default')
            return dd

        dd = {}
        for k, v in self.environ.items():
            if k == 'default':
                continue
            for kk, vv in v.items():
                dd[kk] = vv
        return dd

    @staticmethod
    def get_product_root(root=None, git=None):
        ''' Get the sdss product root used for svn/git products

        Attempts to extract the root directory for SDSS-installed git/svn products.
        Uses the following environment variables in order of precendence:
        PRODUCT_ROOT, SDSS_SVN_ROOT, SDSS_INSTALL_PRODUCT_ROOT, SDSS_PRODUCT_ROOT,
        SDSS4_PRODUCT_ROOT. If no root is found uses one directory up from SAS_BASE_DIR.

        Parameters:
            root (str):
                An absolute directory path to override as the product root
            git (bool):
                If True, looks for SDSS_GIT_ROOT environment variable as product root.

        Returns:
            The directory path to sdss-installed svn/git products
        '''

        # override with an input root directory
        if root:
            return root

        # use an existing $PRODUCT_ROOT envvar
        product_root = os.getenv("PRODUCT_ROOT", None)
        if product_root:
            return product_root

        # check in the config for a product root definition
        product_root = cfg_params.get("PRODUCT_ROOT", None)
        if product_root:
            return product_root

        # attempt to extract a product root from a variety of environment variables
        repo_root = 'SDSS_GIT_ROOT' if git else 'SDSS_SVN_ROOT'
        product_root = os.getenv(repo_root, os.getenv(
            "SDSS_INSTALL_PRODUCT_ROOT", os.getenv("SDSS4_PRODUCT_ROOT", None)))
        if not product_root:
            product_root = os.getenv("SAS_BASE_DIR").rsplit('/', 1)[0]

        return product_root

    def set_product_root(self, root=None, git=None):
        ''' Sets the sdss product root used for svn/git products

        Sets the root directory for SDSS-installed git/svn products as
        the $PRODUCT_ROOT environment variable.  Attempts to find a viable $PRODUCT_ROOT
        using ``get_product_method``.  Viable product roots in order of precendence:
        SDSS_SVN_ROOT, SDSS_INSTALL_PRODUCT_ROOT, SDSS_PRODUCT_ROOT, SDSS4_PRODUCT_ROOT.
        If no root is found uses one directory up from SAS_BASE_DIR.

        Parameters:
            root (str):
                An absolute directory path to override as the product root
            git (bool):
                If True, looks for SDSS_GIT_ROOT environment variable as product root.

        '''
        product_root = self.get_product_root(root=root, git=git)
        os.environ['PRODUCT_ROOT'] = product_root
        self.productroot_dir = product_root

    def write_old_paths_inifile(self):
        ''' Write out an old sdss_paths ini file '''

        paths_dir = os.path.join(self.treedir, 'data/sdss_paths.ini')
        with open(paths_dir, 'w') as f:
            f.write('# Paths for SDSS files. Each file type is given a template full path.\n')
            f.write('# \n')
            f.write('# This file has been deprecated as of tree/3.0.0 and sdss_access/1.0.0 \n')
            f.write('# It should not be updated manually.  Use the tree.write_olds_paths method in \n')
            f.write('# the python tree code to generate a new version of this file as needed.\n')
            f.write('# \n')
            f.write('\n')
            f.write("[paths]\n")
            for name, template in self.paths.items():
                # switch special functions back to %
                template = template.replace('@', '%')
                # write out path, template
                f.write('{0} = {1}\n'.format(name, template))


def get_tree_dir(uproot_with=None):
    ''' Return the path to the tree product directory

    Parameters:
        uproot_with (str):
            A new TREE_DIR path used to override an existing TREE_DIR environment variable

    Returns:
        The path to the tree python product directory
    '''
    treedir = os.environ.get('TREE_DIR', None) if not uproot_with else uproot_with
    if not treedir:
        treefilepath = os.path.dirname(os.path.abspath(__file__))
        if 'python/' in treefilepath:
            treedir = treefilepath.rsplit('/', 2)[0]
        else:
            treedir = treefilepath
        treedir = treefilepath
        os.environ['TREE_DIR'] = treedir
    return treedir
