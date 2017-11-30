
.. _intro:

Introduction to tree
===============================

The SAS Tree defines the directory structure in which all SDSS data files live.  See the :ref:`installation <install>` instructions.

This product provides a Python package version of the tree.  To use the tree, and set up its
environment variables, you may simply import it::

    # import the tree
    from tree import Tree

    # plant a new tree
    my_tree = Tree()

When you plant a new tree, the first thing it tries to do is set a `TREE_DIR` and `SAS_BASE_DIR` environment variable.
`Tree` always first checks for already-defined environment variables in the users environment, and uses those if found.
Otherwise it sets default locations for `TREE_DIR` and `SAS_BASE_DIR`.  By default, it will load all the paths set within
the ``sdsswork`` configuration and populate your local Python environment, `os.environ`, if they are not currently found.

To only load a subset of environment variables, use the `key` keyword argument.

::

    # only load MaNGA environment variables
    my_tree = Tree(key='manga')

    # load MaNGA and eBOSS
    my_tree = Tree(key=['eboss', 'manga'])

The environment variables for the specified keys are now loaded into your Python `os` environment::

    import os
    os.environ['MANGA_SPECTRO_REDUX']

You can load a new section into an existing tree with ``add_limbs``::

    # adds the APO tree section into your os environment
    my_tree.add_limbs(key='apo')

You can load a tree with a different configuration. ::

    dr15_tree = Tree(config='dr15')

Instantiating a tree in this way will not overwrite any existing, or prior set, environment variables.  To
update existing tree environment variables after loading one configuration within the same session, you
can use ``replant_tree``::

    # load the default tree
    my_tree = Tree()

    # switch to the dr15 tree
    my_tree.replant_tree(config='dr15')



.. _tree-api:

Reference/API
^^^^^^^^^^^^^

.. rubric:: Class

.. autosummary:: tree.Tree

.. rubric:: Methods

.. autosummary::

    tree.Tree.add_limbs
    tree.Tree.list_keys
    tree.Tree.replant_tree

