# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-11-29 10:28:58
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-11-29 12:13:40

from __future__ import print_function, division, absolute_import
import pytest
from tree.tree import Tree
import six


@pytest.fixture()
def tree():
    t = Tree()
    yield t
    t = None


class TestTree(object):

    def test_load(self, tree):
        tree
        assert tree.treedir is not None
        assert isinstance(tree.treedir, six.string_types)
        assert tree.environ is not None

