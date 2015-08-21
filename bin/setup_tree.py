#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# $Id$
#
"""Create files that can be used to set environment variables.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
#
# Top-level definitions.
#
__author__ = 'Benjamin Weaver <benjamin.weaver@nyu.edu>'
__version__ = '$Revision$'.split(': ')[1].split()[0]
__all__ = [ ]
__docformat__ = 'restructuredtext en'
#
# Modules
#
import argparse
from collections import OrderedDict
import ConfigParser
import glob
import os
import os.path
import sys
#
# to_file()
#
def to_file(env,header='',setenv='setenv {0} {1}'):
    """Convert config file data to module file.

    Parameters
    ----------
    env : collections.OrderedDict
        A mapping containing all the configuration file data.
    header : str
        String to add to the header of the file produced.
    setenv : str
        The method for setting environment variables in this file type.

    Returns
    -------
    lines : str
        A string representation of the file.
    """
    if len(header) == 0:
        lines = """#
# This file sets up tree/{0}.
#
""".format(env['default']['name'])
    else: lines = header.format(**env['default'])
    for section in env:
        if section == 'default': continue
        lines += """#
# {0}
#
""".format(section)
        setenvs = list()
        for k in env[section]: setenvs.append(setenv.format(k,env[section][k]))
        lines += "\n".join(setenvs)
        lines += "\n"
    return lines
#
# parse_cfg()
#
def parse_cfg(cfg,root):
    """Parse a tree configuration file.

    Parameters
    ----------
    cfg : ConfigParser.ConfigParser
        A ``ConfigParser`` object.
    root : str
        The value of ``$SAS_BASE_DIR``.

    Returns
    -------
    env : collections.OrderedDict
        A mapping containing all the configuration file data
    """
    env = OrderedDict()
    replace = '@FILESYSTEM@'
    env['default'] = cfg.defaults()
    if env['default']['FILESYSTEM'] == replace: env['default']['FILESYSTEM'] = root
    env['default']['current'] = env['default']['current'] == 'True'
    for sec in cfg.sections():
        env[sec] = OrderedDict()
        for opt in cfg.options(sec):
            if opt in env['default']: continue
            val = cfg.get(sec,opt)
            print("section=%r opt=%r val=%r" % (sec,opt,val))
            if val.find(replace) == 0: val = val.replace(replace,root)
            env[sec][opt] = val
    return env
#
# Main function
#
def main():
    """Program to run if called as an executable.
    """
    #
    # Get options
    #
    parser = argparse.ArgumentParser(description=__doc__,prog=os.path.basename(sys.argv[0]))
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
        help='Print extra information.')
    parser.add_argument('-r', '--root', action='store', dest='root',
        default=os.getenv('SAS_BASE_DIR'),
        help='Override the value of $SAS_BASE_DIR.',metavar='SAS_BASE_DIR')
    parser.add_argument('-t', '--treedir', action='store', dest='treedir',
        default=os.getenv('TREE_DIR'),
        help='Override the value of $TREE_DIR.',metavar='TREE_DIR')
    options = parser.parse_args()

    #
    # Configure output files
    #
    tcshheader = """# Set up tree/{name} for (t)csh.
setenv TREE_DIR """ + options.treedir.rstrip('/') + """
setenv TREE_VER {name}
setenv PATH $TREE_DIR/bin:$PATH
"""
    bashheader = """# Set up tree/{name} for (ba)sh.
export TREE_DIR=""" + options.treedir.rstrip('/') + """
export TREE_VER={name}
export PATH=$TREE_DIR/bin:$PATH
"""
    moduleheader = """#%Module1.0
proc ModulesHelp {{ }} {{
    global product version
    puts stderr "This module adds $product $version to various paths"
}}
set product tree
set version {name}
conflict $product
module-whatis   "Sets up $product $version in your environment"

set PRODUCT_DIR """ + options.treedir.rstrip('/') + """
setenv [string toupper $product]_DIR $PRODUCT_DIR
setenv [string toupper $product]_VER $version
prepend-path PATH $PRODUCT_DIR/bin
"""
    modulesversion = """#%Module1.0
set ModulesVersion {name}
"""
    outputs = {
        'tcsh':{
            'ext':'.csh',
            'header':tcshheader,
            'setenv':'setenv {0} {1}'},
        'bash':{
            'ext':'.sh',
            'header':bashheader,
            'setenv':'export {0}={1}'},
        'module':{
            'ext':'.module',
            'header':moduleheader,
            'setenv':'setenv {0} {1}'},
        }
    #
    # Find the data directory
    #
    datadir = os.path.join(options.treedir,'data')
    etcdir = os.path.join(options.treedir,'etc')
    if not os.path.exists(datadir):
        datadir = os.path.join('..','data')
        etcdir = '.'
        if not os.path.exists(datadir):
            print("Could not find a data directory!")
            return 1
    #
    # Read the configuration files
    #
    for cfgfile in glob.glob(os.path.join(datadir,'*.cfg')):
        cfg = ConfigParser.SafeConfigParser()
        cfg.optionxform = str
        cfg.read(cfgfile)
        env = parse_cfg(cfg,options.root)
        if options.verbose:
            print(env)
        for output in outputs:
            filedata = to_file(env,outputs[output]['header'],outputs[output]['setenv'])
            filename = os.path.join(etcdir, env['default']['name']+outputs[output]['ext'])
            with open(filename,'w') as f: f.write(filedata)
            if output == 'module' and env['default']['current']:
                versionname = os.path.join(etcdir, '.version')
                with open(versionname,'w') as f: f.write(modulesversion.format(**env['default']))
    return 0
#
#
#
if __name__ == '__main__':
    sys.exit(main())
