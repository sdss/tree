#!usr/bin/env python
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
import time
import re
import importlib.util


def _remove_link(link):
    ''' Remove a symlink if it exists

    Parameters:
        link (str):
            The symlink filepath
    '''
    if os.path.islink(link):
        os.remove(link)


def make_symlink(src, link):
    '''create a symlink

    Parameters:
        src (str):
            The fullpath source of the symlink
        link (str):
            The symlink file path
    '''
    _remove_link(link)
    os.symlink(src, link)


def create_index_table(environ, envdir):
    ''' create an html table

    Parameters:
        environ (dict):
            A tree environment dictionary
        envdir (str):
            The filepath for the env directory
    Returns:
        An html table definition string
    '''

    table_header = """<table id="list" cellpadding="0.1em" cellspacing="0">
<colgroup><col width="55%"/><col width="20%"/><col width="25%"/></colgroup>
<thead>
    <tr><th><a href="?C=N&O=A">File Name</a>&nbsp;<a href="?C=N&O=D">&nbsp;&darr;&nbsp;</a></th><th><a href="?C=S&O=A">File Size</a>&nbsp;<a href="?C=S&O=D">&nbsp;&darr;&nbsp;</a></th><th><a href="?C=M&O=A">Date</a>&nbsp;<a href="?C=M&O=D">&nbsp;&darr;&nbsp;</a></th></tr>
</thead><tbody>
    <tr><td><a href="../">Parent directory/</a></td><td>-</td><td>-</td></tr>"""
    table_footer = """</tbody></table>"""

    # create table
    table = table_header

    # loop over the environment
    for section, values in environ.items():
        if section == 'default':
            continue

        for tree_name, tree_path in values.items():
            skipmsg = 'Skipping {0} for {1}'.format(tree_name, section)
            if '_ROOT' in tree_name:
                continue

            # create the src and target links
            src = tree_path
            link = os.path.join(envdir, tree_name.upper())

            # get the local time of the symlink
            try:
                stattime = time.strftime('%d-%b-%Y %H:%M', time.localtime(os.stat(src).st_mtime))
            except OSError:
                print("{0} does not appear to exist, skipping...".format(src))
                _remove_link(link)
                continue

            # skip the sas_base_dir
            if section == 'general' and 'SAS_BASE_DIR' in tree_name:
                print(skipmsg)
                continue

            # only create symlinks
            if section == 'general' and tree_name in ['CAS_LOAD', 'STAGING_DATA']:
                # only create links here if the target exist
                if os.path.exists(src):
                    make_symlink(src, link)
                else:
                    print(skipmsg)
            else:
                print('Processing {0} for {1}'.format(tree_name, section))
                make_symlink(src, link)

            # create the table entry
            if os.path.exists(link):
                table += '    <tr><td><a href="{0}/">{0}/</a></td><td>-</td><td>{1}</td></tr>\n'.format(tree_name.upper(), stattime)

    table += table_footer
    return table


def create_index_page(environ, defaults, envdir):
    ''' create the env index html page

    Builds the index.html page containing a table of symlinks
    to datamodel directories

    Parameters:
        environ (dict):
            A tree environment dictionary
        defaults (dict):
            The defaults dictionary from environ['default']
        envdir (str):
            The filepath for the env directory
    Returns:
        A string defintion of an html page
    '''

    # header of index file
    header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><meta name="viewport" content="width=device-width"/><meta http-equiv="content-type" content="text/html; charset=utf-8"/><style type="text/css">body,html {{background:#fff;font-family:"Bitstream Vera Sans","Lucida Grande","Lucida Sans Unicode",Lucidux,Verdana,Lucida,sans-serif;}}tr:nth-child(even) {{background:#f4f4f4;}}th,td {{padding:0.1em 0.5em;}}th {{text-align:left;font-weight:bold;background:#eee;border-bottom:1px solid #aaa;}}#list {{border:1px solid #aaa;width:100%%;}}a {{color:#a33;}}a:hover {{color:#e33;}}</style>
<link rel="stylesheet" href="{url}/css/sas.css" type="text/css"/>
<title>Index of /sas/{name}/env/</title>
</head><body><h1>Index of /sas/{name}/env/</h1>
"""

    # footer of index file
    footer = """<h3><a href='{url}/sas/'>{location}</a></h3>
<p>This directory contains links to the contents of
environment variables defined by the tree product, version {name}.
To examine the <em>types</em> of files contained in each environment variable
directory, visit <a href="/datamodel/files/">the datamodel.</a></p>
</body></html>
"""
    # create index html file
    index = header.format(**defaults)
    index += create_index_table(environ, envdir)
    index += footer.format(**defaults)

    return index


def create_env(environ, mirror=None, verbose=None):
    ''' create the env symlink directory structure

    Creates the env folder filled with symlinks to datamodel directories
    for a given tree config file.

    Parameters:
        environ (dict):
            A tree environment dictionary
        mirror (bool):
            If True, use the SAM url location
        verbose (bool):
            If True, print more information
    '''

    defaults = environ['default'].copy()
    defaults['url'] = "https://data.mirror.sdss.org" if mirror else "https://data.sdss.org"
    defaults['location'] = "SDSS-IV Science Archive Mirror (SAM)" if mirror else "SDSS-IV Science Archive Server (SAS)"

    if 'general' not in environ:
        if verbose:
            print("No 'general' section found in tree environ. Skipping env link creation.")
        return

    if 'SAS_ROOT' not in environ['general']:
        if verbose:
            print("No 'SAS_ROOT' found in 'general' tree environ section. Skipping env link creation.")
        return

    if not os.path.exists(environ['general']['SAS_ROOT']):
        if verbose:
            print("{0} doesn't exist, skipping env link creation.".format(environ['general']['SAS_ROOT']))
        return

    if verbose:
        print("Found {0}.".format(environ['general']['SAS_ROOT']))

    # sets and creates envdir
    envdir = os.path.join(environ['general']['SAS_ROOT'], 'env')
    if not os.path.exists(envdir):
        os.makedirs(envdir)
    if not os.access(envdir, os.W_OK):
        return

    # create index html
    index = create_index_page(environ, defaults, envdir)

    # write the index file
    indexfile = os.path.join(envdir, 'index.html')
    with open(indexfile, 'w') as f:
        f.write(index)


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
    sep = '=' if term == 'bash' else ' '

    if term != 'modules':
        hdr = """# Set up tree/{0} for {1}
{2} TREE_DIR{4}{3}
{2} TREE_VER{4}{0}
{2} PATH{4}$TREE_DIR/bin:$PATH
{2} PYTHONPATH{4}$TREE_DIR/python:$PYTHONPATH
                """.format(name, term, base, product_dir, sep)
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

module load sdsstools
prereq sdsstools
module load sdss_access
prereq sdss_access

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


def write_file(environ, term='bash', out_dir=None, tree_dir=None, default=None):
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
        default (str):
            The default config to write into the .version file

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
                    if tree_path.startswith(os.getenv("SAS_BASE_DIR")):
                        f.write(cmd.format(tree_name.upper(), tree_path))

    # write default .version file for modules (or default for lua modules)
    default = default if default else name
    modules_version = write_version(default)
    if term == 'modules' and environ['default']['current'] == 'True':
        # write .version file for tcl
        version_name = os.path.join(out_dir, '.version')
        with open(version_name, 'w') as f:
            f.write(modules_version)


def get_python_path():
    ''' Finds and switches to the tree python package directory '''
    # get the TREE directory
    tree_dir = os.getenv('TREE_DIR', None)
    if not tree_dir:
        path = os.path.dirname(os.path.abspath(__file__))
        tree_dir = os.path.realpath(os.path.join(path, '..'))
    pypath = os.path.join(tree_dir, 'python')

    if pypath not in sys.path:
        sys.path.append(pypath)
    os.chdir(pypath)


def get_tree(config=None):
    ''' Get the tree for a given config

    Parameters:
        config (str):
            The name of the tree config to load

    Returns:
        a Python Tree instance
    '''

    # ensure the tree package is importable
    mod = importlib.util.find_spec('tree')
    if not (mod and mod.origin):
        get_python_path()

    # extract the config format from either XXXX.cfg or full filepath
    has_cfg = re.search(r'(\w+)\.cfg', config)
    if has_cfg:
        config = has_cfg.group()
    from tree.tree import Tree
    tree = Tree(config=config)
    return tree


def copy_modules(filespath=None, modules_path=None, verbose=None, default=None, force=None):
    ''' Copy over the tree module files into your path '''

    # find or define a modules path
    if not modules_path:
        modulepath = os.getenv("MODULEPATH")
        if not modulepath:
            modules_path = input('Enter the root path for your module files:')
        else:
            split_mods = modulepath.split(':')
            if len(split_mods) > 1:
                # select which module paths to use
                items = ['Multiple module paths found. Choose which module paths to use '
                         '(e.g. "1,2") or hit enter for "all". Or "q" to quit: ']
                items += ['{0}. {1}'.format(i + 1, t) for i, t in enumerate(split_mods)] + ['\n']
                msg = '\n'.join(items)
                selected = input(msg) or 'all'
                # check to quit
                if selected == 'q':
                    if verbose:
                        print('Quitting module copy.')
                    return

                # select choices
                choices = range(len(split_mods)) if selected == 'all' else [
                    int(i) - 1 for i in selected.split(',')]

                # loop over selected module paths to install tree
                for choice in choices:
                    mfile = split_mods[choice]
                    # run rest of method
                    copy_modules(filespath=filespath, modules_path=mfile, verbose=verbose,
                                 default=default)

                # exit the function after loop is over
                return
            else:
                modules_path = split_mods[0]
                if verbose:
                    print('Installing tree modules into {0}'.format(modules_path))

    # check for the tree module directory
    tree_mod = os.path.join(modules_path, 'tree')
    if not os.path.isdir(tree_mod):
        if verbose:
            print('Creating module tree directory: {0}'.format(tree_mod))
        os.makedirs(tree_mod)
    elif not force:
        doit = input('{0} already exists! Overwrite? (y/n) \n'.format(tree_mod)) or 'n'
        if doit == 'n':
            return

    # copy the modules into the tree
    if verbose:
        print('Copying modules from {1} into {0}'.format(tree_mod, filespath))
    module_files = glob.glob(os.path.join(filespath, '*.module'))
    for mfile in module_files:
        base = os.path.splitext(os.path.basename(mfile))[0]
        tree_out = os.path.join(tree_mod, base)
        shutil.copy2(mfile, tree_out)

    # copy the default .version into the tree
    version = os.path.join(filespath, '.version')
    if os.path.isfile(version):
        shutil.copy2(version, tree_mod)

    # write default file for lua
    if default:
        defpath = os.path.join(tree_mod, 'default')
        realpath = default
        if os.path.islink(defpath):
            os.unlink(defpath)
        os.symlink(realpath, defpath)


def check_output_dir(output_dir):
    ''' Check the output directory '''

    # check if output directory is within a pip package directory
    if 'site-packages' in output_dir or output_dir.endswith('python/tree/etc'):
        output_dir = os.path.expanduser('~/.tree/environments')

    # create directory if it does not exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    return output_dir


def get_parser():
    ''' Parse the arguments '''

    description = ('Create bash, tsch, and module environment configuration files '
                   'defining relevant variables for accessing data products on '
                   'the SDSS Science Archive Server (SAS)')
    parser = argparse.ArgumentParser(prog='setup_tree.py', description=description)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='Print extra information.', default=False)
    parser.add_argument('-r', '--root', action='store', dest='root', default=os.getenv('SAS_BASE_DIR'),
                        help='Override the environment variable $SAS_BASE_DIR.', metavar='SAS_BASE_DIR')
    parser.add_argument('-t', '--treedir', action='store', dest='treedir', default=os.getenv('TREE_DIR'),
                        help='Override the environment variable $TREE_DIR.', metavar='TREE_DIR')
    parser.add_argument('-m', '--modulesdir', action='store', dest='modulesdir', default=os.getenv('MODULES_DIR'),
                        help='Your modules directory.  Defaults to $MODULES_DIR', metavar='MODULES_DIR')
    parser.add_argument('-e', '--env', action='store_true', dest='env',
                        help='Create tree environment symlinks.', default=False)
    parser.add_argument('-i', '--mirror', action='store_true', dest='mirror',
                        help='Use the mirror site (SAM) instead.')
    parser.add_argument('-o', '--only', action='store', dest='only', metavar='[xxx].cfg',
                        default=None, help='create links for only the specified tree config.')
    parser.add_argument('-d', '--default', action='store', dest='default', default='sdsswork',
                        help='Default config version to write into the .version file. Defaults to "sdsswork"')
    parser.add_argument('-p', '--path', action='store', dest='path', default=None,
                        help='Custom output path to copy environment files')
    parser.add_argument('-f', '--force', action='store_true', dest='force',
                        help='Force overwrite of existing modulefiles', default=False)

    return parser


def main(opts):

    # check for a treedir; if none found, set path to the parent directory
    if not opts.treedir:
        # look for installed python module
        mod = importlib.util.find_spec('tree')
        if mod and mod.origin:
            opts.treedir = os.path.dirname(mod.origin)
        else:
            opts.treedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        os.environ['TREE_DIR'] = opts.treedir

    # get directories
    datadir = os.path.join(opts.treedir, 'data')
    etcdir = opts.path if opts.path else os.path.join(opts.treedir, 'etc')
    etcdir = check_output_dir(etcdir)

    if opts.verbose:
        print('TREE_DIR: ', opts.treedir)
        print("Data Directory : ", datadir)
        print('Output Directory: ', etcdir)

    # config files
    configs = glob.glob(os.path.join(datadir, '*.cfg'))
    if not configs:
        print('No config files found in {0}.  Cannot proceed with tree setup. '
              'Check for correct TREE_DIR.'.format(datadir))
        return

    # check for the SAS_BASE_DIR
    check_sas_base_dir(root=opts.root)

    # Read and write the configuration files
    for cfgfile in configs:
        # skip basework config
        if 'basework' in cfgfile:
            continue

        tree = get_tree(config=cfgfile)
        # create env symlinks or write out tree module/bash files
        if opts.env:
            # skip creating the environ if a specific config if specified
            if opts.only and opts.only not in cfgfile:
                continue
            create_env(tree.environ, mirror=opts.mirror)
        else:
            write_file(tree.environ, term='modules', out_dir=etcdir, tree_dir=opts.treedir, default=opts.default)
            write_file(tree.environ, term='bash', out_dir=etcdir, tree_dir=opts.treedir)
            write_file(tree.environ, term='tsch', out_dir=etcdir, tree_dir=opts.treedir)

    # check for files
    module_files = glob.glob(os.path.join(etcdir, '*.module'))
    if not any(module_files):
        print('No module files created in {0}'.format(etcdir))
    else:
        print('Environment files created in: {0}'.format(etcdir))

    # Setup the modules
    print('Copying module files...')
    copy_modules(filespath=etcdir, modules_path=opts.modulesdir, verbose=opts.verbose, default=opts.default, force=opts.force)


if __name__ == '__main__':

    # parse arguments
    opts = get_parser().parse_args()
    main(opts)
