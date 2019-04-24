# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-07-14 14:31:36
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-07-14 19:03:32

from __future__ import print_function, division, absolute_import
import sys
import os
import argparse
import glob
import shutil


def check_sas_base_dir(root=None):
    ''' Check for the SAS_BASE_DIR environment variable

    Will set the SAS_BASE_DIR in your local environment
    or prompt you to define one if is undefined

    Parameters:
        root (str):
            Optional override of the SAS_BASE_DIR envvar

    '''
    sasbasedir = root or os.getenv("SAS_BASE_DIR")
    if not sasbasedir:
        sasbasedir = input('Enter a path for SAS_BASE_DIR: ')
    os.environ['SAS_BASE_DIR'] = sasbasedir


def write_header(term='bash', tree_dir=None, name=None):
    ''' Write proper file header in a given shell format

    Parameters:
        term (str):
            The type of shell header to write, can be "bash", "tsch", or "modules"
        tree_dir (str):
            The path to this repository
        name (str):
            The name of the configuration

    Returns:
        A string header to insert
    '''

    assert term in ['bash', 'tsch', 'modules'], 'term must be either bash, tsch, or module'

    product_dir = tree_dir.rstrip('/')
    base = 'export' if term == 'bash' else 'setenv'

    if term != 'modules':
        hdr = """# Set up tree/{0} for {1}
{2} TREE_DIR {3}
{2} TREE_VER {1}
{2} PATH $TREE_DIR/bin:$PATH
{2} PYTHONPATH $TREE_DIR/python:$PYTHONPATH
                """.format(name, term, base, product_dir)
    else:
        hdr = """#%Module1.0
proc ModulesHelp {{ }} {{
    global product version
    puts stderr "This module adds $product/$version to various paths"
}}
set name tree
set product tree
set version {1}
conflict $product
module-whatis "Sets up $product/$version in your environment"

set PRODUCT_DIR {0}
setenv [string toupper $product]_DIR $PRODUCT_DIR
setenv [string toupper $product]_VER $version
prepend-path PATH $PRODUCT_DIR/bin
prepend-path PYTHONPATH $PRODUCT_DIR/python

                """.format(product_dir, name)

    return hdr.strip()


def write_version(name):
    ''' Make the default modules version string '''
    modules_version = "#%Module1.0\nset ModulesVersion {0}".format(name)
    return modules_version


def write_file(environ, term='bash', out_dir=None, tree_dir=None):
    ''' Write a tree environment file

    Loops over the tree environ and writes them out to a bash, tsch, or
    modules file

    Parameters:
        environ (dict):
            The tree dictionary environment
        term (str):
            The type of shell header to write, can be "bash", "tsch", or "modules"
        tree_dir (str):
            The path to this repository
        out_dir (str):
            The output path to write the files (default is etc/)

    '''

    # get the proper name, header and file extension
    name = environ['default']['name']
    header = write_header(term=term, name=name, tree_dir=tree_dir)
    exts = {'bash': '.sh', 'tsch': '.csh', 'modules': '.module'}
    ext = exts[term]

    # shell command
    if term == 'bash':
        cmd = 'export {0}={1}\n'
    else:
        cmd = 'setenv {0} {1}\n'

    # write the environment config files
    filename = os.path.join(out_dir, name + ext)
    with open(filename, 'w') as f:
        f.write(header + '\n')
        for key, values in environ.items():
            if key != 'default':
                # write separator
                f.write('#\n# {0}\n#\n'.format(key))
                # write tree names and paths
                for tree_name, tree_path in values.items():
                    f.write(cmd.format(tree_name.upper(), tree_path))

    # write default .version file for modules
    modules_version = write_version(name)
    if term == 'modules' and environ['default']['current']:
        version_name = os.path.join(out_dir, '.version')
        with open(version_name, 'w') as f:
            f.write(modules_version)


def get_tree(config=None):
    ''' Get the tree for a given config

    Parameters:
        config (str):
            The name of the tree config to load

    Returns:
        a Python Tree instance
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    pypath = os.path.realpath(os.path.join(path, '..', 'python'))
    if pypath not in sys.path:
        sys.path.append(pypath)
    os.chdir(pypath)
    from tree.tree import Tree
    tree = Tree(config=config)
    return tree


def copy_modules(filespath=None, modules_path=None, verbose=None):
    ''' Copy over the tree module files into your path '''

    # find or define a modules path
    if not modules_path:
        modulepath = os.getenv("MODULEPATH")
        if not modulepath:
            modules_path = input('Enter the root path for your module files:')
        else:
            split_mods = modulepath.split(':')
            if len(split_mods) > 1:
                if verbose:
                    print('Multiple module paths found.  Using top one: {0}'.format(split_mods[0]))
            modules_path = split_mods[0]

    # check for the tree module directory
    tree_mod = os.path.join(modules_path, 'tree')
    if not os.path.isdir(tree_mod):
        os.makedirs(tree_mod)

    # copy the modules into the tree
    if verbose:
        print('Copying modules from etc/ into {0}'.format(tree_mod))
    module_files = glob.glob(os.path.join(filespath, '*.module'))
    for mfile in module_files:
        base = os.path.splitext(os.path.basename(mfile))[0]
        tree_out = os.path.join(tree_mod, base)
        shutil.copy2(mfile, tree_out)

    # copy the default version into the tree
    version = os.path.join(filespath, '.version')
    if os.path.isfile(version):
        shutil.copy2(version, tree_mod)


def parse_args():
    ''' Parse the arguments '''

    parser = argparse.ArgumentParser(prog='setup_tree_modules', usage='%(prog)s [opts]')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='Print extra information.', default=False)
    parser.add_argument('-r', '--root', action='store', dest='root', default=os.getenv('SAS_BASE_DIR'),
                        help='Override the value of $SAS_BASE_DIR.', metavar='SAS_BASE_DIR')
    parser.add_argument('-t', '--treedir', action='store', dest='treedir', default=os.getenv('TREE_DIR'),
                        help='Override the value of $TREE_DIR.', metavar='TREE_DIR')
    parser.add_argument('-m', '--modulesdir', action='store', dest='modulesdir', default=os.getenv('MODULES_DIR'),
                        help='Your modules directory', metavar='MODULES_DIR')

    opts = parser.parse_args()

    return opts


def main(args):

    # parse arguments
    opts = parse_args()

    # get directories
    datadir = os.path.join(opts.treedir, 'data')
    etcdir = os.path.join(opts.treedir, 'etc')

    # config files
    configs = glob.glob(os.path.join(datadir, '*.cfg'))

    # check for the SAS_BASE_DIR
    check_sas_base_dir(root=opts.root)

    # Read and write the configuration files
    for cfgfile in configs:
        tree = get_tree(config=cfgfile)
        write_file(tree.environ, term='modules', out_dir=etcdir, tree_dir=opts.treedir)
        write_file(tree.environ, term='bash', out_dir=etcdir, tree_dir=opts.treedir)
        write_file(tree.environ, term='tsch', out_dir=etcdir, tree_dir=opts.treedir)

    # Setup the modules
    copy_modules(filespath=etcdir, verbose=opts.verbose)


if __name__ == '__main__':
    main(sys.argv[1:])
