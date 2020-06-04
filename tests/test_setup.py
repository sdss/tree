# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_setup.py
# Project: tests
# Author: Brian Cherinka
# Created: Saturday, 13th April 2019 6:11:21 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2019 Brian Cherinka
# Last Modified: Monday, 6th April 2020 6:46:44 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import os
import subprocess
import pytest
import glob
import sys
from tree import Tree

setuppath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../bin/setup_tree.py'))


@pytest.fixture()
def tree(faketree):
    # create the fake tree
    t = Tree()
    yield t
    t = None


def test_intemp(tree):
    assert 'treetmp' in tree.environ['general']['SAS_BASE_DIR']
    treedir = os.getenv('TREE_DIR')
    assert 'treetmp' in treedir
    assert 'treetmp' in os.getenv('MODULES_DIR')
    assert os.path.exists(os.path.join(treedir, 'etc'))
    assert os.path.exists(os.path.join(treedir, 'data'))
    files = glob.glob(os.path.join(treedir, 'data/*.cfg'))
    assert len(files) > 1


# def run_cmd(args=[], user_input=''):
#     process = subprocess.Popen(['python', setuppath] + args, universal_newlines=True,
#                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, __ = process.communicate(input=user_input)
#     return stdout

def run_cmd(args=[], user_input=''):
    if sys.version_info.major == 2 or (sys.version_info.major == 3 and sys.version_info.minor < 7):
        out = subprocess.check_output(['python', setuppath] + args,
                                      universal_newlines=True, input=user_input)
    else:
        process = subprocess.run(['python', setuppath] + args, universal_newlines=True,
                                 input=user_input, capture_output=True)
        out = process.stdout
    return out


def read_index(path):
    with open(path, 'r') as f:
        data = f.read()
    return data


def assert_stuff(envdir, name):
    index = os.path.join(envdir, 'index.html')
    assert os.path.exists(index)
    page = read_index(index)
    assert name.upper() in page


@pytest.mark.parametrize('name', [('MANGA_HI'), ('MANGA_SPECTRO_REDUX')], ids=['mangahi', 'redux'])
def test_envlinks(tree, name):
    assert os.path.isfile(setuppath)
    envdir = os.path.join(tree.environ['general']['SAS_BASE_DIR'], 'dr15/env')
    stdout = run_cmd(args=['-e'])
    assert os.path.exists(envdir) is True
    assert 'Processing {0}'.format(name) in str(stdout)
    linkdir = os.path.join(envdir, name.upper())
    assert os.path.isdir(linkdir)
    assert os.path.islink(linkdir)
    assert_stuff(envdir, name)


@pytest.mark.parametrize('name', [('MANGA_HI'), ('MANGA_SPECTRO_REDUX')], ids=['mangahi', 'redux'])
def test_env_only(tree, name):
    dr15envdir = os.path.join(tree.environ['general']['SAS_BASE_DIR'], 'dr15/env')
    dr14envdir = os.path.join(tree.environ['general']['SAS_BASE_DIR'], 'dr14/env')
    stdout = run_cmd(args=['-e', '-o', 'dr14'])
    assert os.path.exists(dr14envdir) is True
    assert os.path.exists(dr15envdir) is False
    if 'HI' in name:
        assert 'Processing {0}'.format(name) not in str(stdout)
    else:
        assert 'Processing {0}'.format(name) in str(stdout)
        assert_stuff(dr14envdir, name)


@pytest.mark.parametrize('mirror, exp', [(False, 'SDSS-IV Science Archive Server (SAS)'),
                                         (True, 'SDSS-IV Science Archive Mirror (SAM)')])
def test_env_mirror(tree, mirror, exp):
    envdir = os.path.join(tree.environ['general']['SAS_BASE_DIR'], 'dr15/env')
    args = ['-e', '-i'] if mirror else ['-e']
    stdout = run_cmd(args=args)
    index = os.path.join(envdir, 'index.html')
    page = read_index(index)
    assert exp in page


@pytest.mark.parametrize('config', [('dr15'), ('dr14'), ('sdsswork'), ('sdss5')])
def test_create_files(tree, config):
    etcdir = os.path.join(os.getenv('TREE_DIR'), 'etc')
    assert os.path.exists(etcdir)
    files = glob.glob(os.path.join(etcdir, '*.*'))
    assert len(files) == 0
    stdout = run_cmd(args=[])
    files = glob.glob(os.path.join(etcdir, '*.*'))
    assert len(files) > 1
    assert os.path.exists(os.path.join(etcdir, config + '.sh'))
    assert os.path.exists(os.path.join(etcdir, config + '.csh'))
    assert os.path.exists(os.path.join(etcdir, config + '.module'))

    # ensure modules were copied
    moduledir = os.path.join(os.getenv('MODULES_DIR'), 'tree')
    files = glob.glob(os.path.join(moduledir, '*'))
    assert len(files) > 0
    assert os.path.exists(os.path.join(moduledir, config))


@pytest.fixture()
def resetmod(monkeypatch):
    mdir = os.environ.get('MODULES_DIR')
    base = os.path.dirname(mdir)
    monkeypatch.setenv("MODULES_DIR", '')
    os.makedirs(os.path.join(base, 'crap'))
    newpath = os.path.join(base, 'crap') + ':' + mdir
    monkeypatch.setenv('MODULEPATH', newpath)
    os.makedirs(os.path.join(mdir, 'tree'))


def assert_paths(path, config):
    files = glob.glob(os.path.join(path, '*'))
    assert os.path.exists(path)
    assert len(files) >= 0
    assert os.path.exists(os.path.join(path, config))


def assert_no_paths(path, config, haspath=False):
    files = glob.glob(os.path.join(path, '*'))
    assert os.path.exists(path) if haspath else not os.path.exists(path)
    assert len(files) == 0


@pytest.mark.parametrize('config, inputs',
                         [('dr15', '1'),
                          ('sdsswork', '2\ny\n'),
                          ('sdsswork', 'all\ny\n')], ids=['copy1', 'copy2', 'copyall'])
def test_emptymodulepath(tree, resetmod, config, inputs):

    modulepath = os.environ.get('MODULEPATH')
    split_mods = modulepath.split(':')
    for mpath in split_mods:
        if 'crap' in mpath:
            assert not os.path.exists(os.path.join(mpath, 'tree'))
        else:
            assert os.path.exists(os.path.join(mpath, 'tree'))

    stdout = run_cmd(args=[], user_input=inputs)

    if inputs == '1':
        # assert only first module path gets copied
        # crap path
        path = os.path.join(split_mods[0], 'tree')
        assert_paths(path, config)

        # module path
        path = os.path.join(split_mods[1], 'tree')
        assert_no_paths(path, config, haspath=True)

    elif inputs.startswith('2'):
        # assert only second module path gets copied
        # crap path
        path = os.path.join(split_mods[0], 'tree')
        assert_no_paths(path, config)

        # module path
        path = os.path.join(split_mods[1], 'tree')
        assert_paths(path, config)
    elif inputs.startswith('all'):
        # assert both module paths get copied
        for mpath in split_mods:
            path = os.path.join(mpath, 'tree')
            assert_paths(path, config)
