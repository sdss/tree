#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# $Id$
#
"""Create environment variable symlinks.
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
import time
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
    if env['default']['FILESYSTEM'] == replace:
        env['default']['FILESYSTEM'] = root
    # env['default']['install'] = os.path.dirname(os.path.dirname(os.getenv('INSTALL_DIR')))
    env['default']['current'] = env['default']['current'] == 'True'
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
#
#
def make_link(src,link,options):
    """Encapsulate link creation
    """
    debug = options.test or options.verbose
    if debug:
        print("{0} -> {1}".format(link,src))
    if not options.test:
        if os.path.islink(link):
            os.remove(link)
        os.symlink(src,link)
    return
#
# Main function
#
def main():
    """Program to run if called as an executable."""
    #
    # Get options
    #
    parser = argparse.ArgumentParser(description=__doc__,prog=os.path.basename(sys.argv[0]))
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
        help='Print extra information.')
    parser.add_argument('-f', '--force', action='store_true', dest='force',
        help='Force the creation of some symlinks.')
    parser.add_argument('-t', '--test', action='store_true', dest='test',
        help='Only show what would be done (implies --verbose).')
    parser.add_argument('-o', '--only', action='store', dest='only',
        default='ALL', metavar='TREE',
        help='Create links for only TREE.')
    parser.add_argument('-r', '--root', action='store', dest='root',
        default=os.path.dirname(os.getenv('SAS_ROOT')),
        help='Override the value of $SAS_ROOT.',metavar='DIR')
    options = parser.parse_args()
    debug = options.test or options.verbose
    #
    # Find the data directory
    #
    datadir = os.path.join(os.getenv('TREE_DIR'),'data')
    if not os.path.exists(datadir):
        datadir = os.path.join('..','data')
        if not os.path.exists(datadir):
            print("Could not find a data directory!")
            sys.exit(1)
    #
    # Set up index file
    #
    header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head><title>Index of /sas/{0}/env/</title></head>
<body style="background-color:white;">
<h1>Index of /sas/{0}/env/</h1><hr /><pre><a href="../">../</a>
"""
    footer = """</pre><hr />
<p>This directory contains links to the contents of
environment variables defined by the tree product, version {0}.
To examine the <em>types</em> of files contained in each environment variable
directory, visit <a href="/datamodel/files/">the datamodel.</a></p>
</body>
</html>
"""
    #
    # Read the configuration files
    #
    for cfgfile in glob.glob(os.path.join(datadir,'*.cfg')):
        cfg = ConfigParser.SafeConfigParser()
        cfg.optionxform = str
        cfg.read(cfgfile)
        env = parse_cfg(cfg,options.root)
        if options.only != 'ALL' and env['default']['name'] != options.only:
            continue
        # if debug:
        #     print(env)
        if os.path.exists(env['general']['SAS_ROOT']):
            if debug:
                print("Found {0}.".format(env['general']['SAS_ROOT']))
            envdir = os.path.join(env['general']['SAS_ROOT'],'env')
            if not os.path.exists(envdir):
                if debug:
                    print("Creating {0}.".format(envdir))
                if not options.test:
                    os.mkdir(envdir)
            index = header.format(env['default']['name'])
            for section in env:
                if section == 'default':
                    continue
                for var in env[section]:
                    if var.find('_ROOT') > 0:
                        continue
                    src = env[section][var]
                    link = os.path.join(envdir,var)
                    spaces = ' '*(52 - (len(var)+1))
                    try:
                        stattime = time.strftime('%d-%b-%Y %H:%M',time.localtime(os.stat(src).st_mtime))
                    except OSError:
                        print("{0} does not appear to exist, skipping...".format(src))
                        continue
                    if section == 'general' and var in ('CAS_LOAD','STAGING_DATA'):
                        #
                        # For this section only, install links only if their
                        # targets exist. The --force option overrides this.
                        #
                        if options.force or os.path.exists(src):
                            make_link(src,link,options)
                            index += '<a href="{0}/">{0}/</a>{1}{2}                   -\n'.format(var,spaces,stattime)
                    else:
                        make_link(src,link,options)
                        index += '<a href="{0}/">{0}/</a>{1}{2}                   -\n'.format(var,spaces,stattime)
            index += footer.format(env['default']['name'])
            indexfile = os.path.join(envdir,'index.html')
            if debug:
                print("Creating {0}.".format(indexfile))
                print(index)
            if not options.test:
                with open(indexfile,'w') as f:
                    f.write(index)
        else:
            print("{0} doesn't exist, skipping env link creation.".format(env['general']['SAS_ROOT']))
    return
#
#
#
if __name__ == '__main__':
    main()

