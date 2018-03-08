# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-11-29 10:28:58
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-03-08 10:58:37

from __future__ import print_function, division, absolute_import
import pytest
from tree.tree import Tree
import six
import os


@pytest.fixture()
def tree():
    t = Tree()
    yield t
    t = None


class TestTree(object):

    def test_load(self, tree):
        assert tree.treedir is not None
        assert isinstance(tree.treedir, six.string_types)
        assert tree.environ is not None
        assert 'APO' in tree.environ
        assert 'sdsswork' == tree.environ['default']['name']

    @pytest.mark.parametrize('keys', [('manga'), ('MANGA'), (['manga', 'apogee'])],
                             ids=['manga', 'capmanga', 'apomanga'])
    def test_load_keys(self, keys):
        t = Tree(key=keys)
        assert 'APO' not in t.environ
        assert 'default' in t.environ
        assert 'general' in t.environ
        keys = keys if isinstance(keys, list) else [keys]
        for key in keys:
            assert key.upper() in t.environ

    @pytest.mark.parametrize('dr', [('dr14')])
    def test_load_dr_config(self, dr):
        t = Tree(config=dr)
        assert dr == t.environ['default']['name']

    @pytest.mark.parametrize('dr', [('dr14')])
    def test_load_with_update(self, tree, dr):
        assert 'sdsswork' in tree.environ['default']['name']
        assert 'mangawork' in tree.environ['MANGA']['manga_root']
        tree = Tree(config=dr, update=True)
        assert dr in tree.environ['default']['name']
        assert dr in tree.environ['MANGA']['manga_root']

    @pytest.mark.parametrize('dr', [('dr14')])
    def test_replant_tree(self, tree, dr):
        assert 'sdsswork' in tree.environ['default']['name']
        assert 'mangawork' in tree.environ['MANGA']['manga_root']
        tree.replant_tree(dr)
        assert dr in tree.environ['default']['name']
        assert dr in tree.environ['MANGA']['manga_root']

    def test_custom_paths_remain(self, monkeypatch):
        # set custom environ variable
        name = 'MANGA_QUICK'
        path = '/tmp/work/manga/quick'
        monkeypatch.setitem(os.environ, name, path)
        assert os.environ[name] == path
        tree = Tree()
        assert os.environ[name] == path
        assert path != tree.environ['MANGA'][name.lower()]

    def test_custom_paths_donotupdate(self, monkeypatch, tree):
        name = 'MANGA_QUICK'
        path = '/tmp/work/manga/quick'
        monkeypatch.setitem(os.environ, name, path)
        assert os.environ[name] == path
        tree.replant_tree('sdsswork')
        assert os.environ[name] != path
        assert os.environ[name] == tree.environ['MANGA'][name.lower()]

    def test_custom_paths_update_with_exclude(self, monkeypatch, tree):
        name = 'MANGA_QUICK'
        path = '/tmp/work/manga/quick'
        monkeypatch.setitem(os.environ, name, path)
        assert os.environ[name] == path
        tree.replant_tree('sdsswork', exclude=['MANGA_QUICK'])
        assert os.environ[name] == path
        assert path != tree.environ['MANGA'][name.lower()]



