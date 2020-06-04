#!/usr/bin/env python
# encoding: utf-8
#
# conftest.py
#


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import shutil
import pytest


def make_dirs(path):
    (path / 'dr14/manga/spectro/redux/v2_1_2').mkdir(parents=True)
    (path / 'dr15/manga/spectro/redux/v2_4_3').mkdir(parents=True)
    (path / 'dr15/manga/spectro/analysis/v2_4_3/2.1.2').mkdir(parents=True)
    (path / 'dr15/manga/HI/v1_0_1').mkdir(parents=True)


@pytest.fixture()
def faketree(monkeypatch, tmp_path):
    # set up temp tree path
    p = tmp_path / "treetmp"
    p.mkdir(parents=True)
    # create fake datamodel directories
    make_dirs(p)
    monkeypatch.setenv('SAS_BASE_DIR', str(p))
    # setup fake config stuff
    treedir = p / 'treedir'
    treedir.mkdir(parents=True)
    # copy data over
    olddatadir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
    shutil.copytree(olddatadir, str(treedir / 'data'))
    (treedir / 'etc').mkdir()
    monkeypatch.setenv('TREE_DIR', str(treedir))
    # setup modulesdir
    mdir = p / 'modules'
    mdir.mkdir(parents=True)
    monkeypatch.setenv('MODULES_DIR', str(mdir))
