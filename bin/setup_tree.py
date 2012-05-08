#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# $Id$
#
"""Create files that can be used to set environment variables.
"""
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
import transfer
#
# csh()
#
def to_file(env,header='',setenv='setenv {0} {1}'):
    """Convert config file data to .

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
    else:
        lines = header.format(**env['default'])
    for section in env:
        if section == 'default':
            continue
        lines += """#
# {0}
#
""".format(section)
        setenvs = list()
        for k in env[section]:
            setenvs.append(setenv.format(k,env[section][k]))
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
        The value of ``$SAS_ROOT``.

    Returns
    -------
    env : collections.OrderedDict
        A mapping containing all the configuration file data
    """
    env = OrderedDict()
    replace = '@FILESYSTEM@'
    env['default'] = cfg.defaults()
    env['default']['FILESYSTEM'] = root
    for sec in cfg.sections():
        env[sec] = OrderedDict()
        for opt in cfg.options(sec):
            if opt in env['default']:
                continue
            val = cfg.get(sec,opt)
            if val.find(replace) == 0:
                val = val.replace(replace,root)
            env[sec][opt] = val
    return env
#
# Main function
#
def main():
    """Program to run if called as an executable."""
    #
    # Get options
    #
    parser = argparse.ArgumentParser(description=__doc__,prog=os.path.basename(sys.argv[0]))
    parser.add_argument('-V','--version',action='version',
        version=("%(prog)s {0}/r{1}".format(transfer.version('$HeadURL$'),
            __version__)),
        help='Print version information and exit.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
        help='Print extra information (sets log level to DEBUG).')
    parser.add_argument('-t', '--test', action='store_true', dest='test',
        help='Do not actually run commands (implies --verbose).')
    parser.add_argument('-r', '--root', action='store', dest='root',
        default=os.getenv('SAS_ROOT'),
        help='Override the value of $SAS_ROOT.',metavar='DIR')
    options = parser.parse_args()
    debug = options.verbose or options.test
    #
    # Configure output files
    #
    eupsheader = """# Set up tree/{name} for EUPS.
envPrepend(PATH,${{PRODUCT_DIR}}/bin)
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

set PRODUCT_DIR "/home/products/NULL/$product/$version"
setenv [string toupper $product]_DIR $PRODUCT_DIR
prepend-path PATH $PRODUCT_DIR/bin
"""
    outputs = {
        'tcsh':{
            'ext':'.csh',
            'header':'# Set up tree/{name} for (t)csh.\n',
            'setenv':'setenv {0} {1}'},
        'bash':{
            'ext':'.sh',
            'header':'# Set up tree/{name} for (ba)sh\n',
            'setenv':'export {0}={1}'},
        'eups':{
            'ext':'.table',
            'header':eupsheader,
            'setenv':'envSet({0},{1})'},
        'module':{
            'ext':'.module',
            'header':moduleheader,
            'setenv':'setenv {0} {1}'},
        }
    #
    # Read the configuration files
    #
    for cfgfile in glob.glob(os.path.join(os.getenv('TREE_DIR'),'data','*.cfg')):
        cfg = ConfigParser.SafeConfigParser()
        cfg.optionxform = str
        cfg.read(cfgfile)
        env = parse_cfg(cfg,options.root)
        # print(env)
        for output in outputs:
            filedata = to_file(env,outputs[output]['header'],outputs[output]['setenv'])
            filename = os.path.join(os.getenv('TREE_DIR'),'etc',
                env['default']['name']+outputs[output]['ext'])
            with open(filename,'w') as f:
                f.write(filedata)
    return
#
#
#
if __name__ == '__main__':
    main()

