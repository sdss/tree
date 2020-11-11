
.. _intro:

Introduction to tree
====================

The SAS Tree defines the directory structure in which all SDSS data files live.  The SAS tree product helps set up all the
SDSS environment variables you need to run SDSS products. The list of currrently available environment variables can be found
:ref:`here <config>`.

This product provides a Python package version of the `.Tree`.  See the :ref:`installation <install>` instructions.
To use the tree, and set up its environment variables, you may simply import it
::

    >>> # import the tree
    >>> from tree import Tree

    >>> # load the default sdsswork tree
    >>> my_tree = Tree()
    >>> my_tree
    Tree(sas_base_dir=/Users/Brian/Work/sdss/sas, config=sdsswork)

When you create a new tree, it will first try to load any default environment module already loaded, identified using the `TREE_VER`
environment variable.  If it cannot find one, it will try to set a `TREE_DIR` and `SAS_BASE_DIR` environment variable.
``Tree`` always first checks for already-defined environment variables in the users environment, and uses those if found.
Otherwise it sets default locations for `TREE_DIR` and `SAS_BASE_DIR`.  The default location for `TREE_DIR` will be the location
of the installed package.  The default location for `SAS_BASE_DIR` will be a new ``sas`` directory in the users home directory.
By default, it will load all the paths set within the ``sdsswork`` configuration and populate your local Python environment,
``os.environ``, if they are not currently found.

To load a different tree environment, simply pass in a new configuration name.
::

    >>> # load the environment for DR15
    >>> my_tree = Tree('dr15')
    >>> my_tree
    Tree(sas_base_dir=/Users/Brian/Work/sdss/sas, config=dr15)

The underlying dictionary of environment variable definitions is accessible via the ``environ`` attribute.  The underlying dictionary
of ``sdss_access`` path templates for the given environment is accessible via the ``paths`` attribute.
::

    >>> # access an environment variable definition
    >>> my_tree.environ['MANGA']['MANGA_SPECTRO_REDUX']
    '/Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux'

    >>> # access a path defintion
    >>> my_tree.paths['mangacube']
    '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}CUBE.fits.gz'

Loading only subsets
--------------------

To only load a subset of environment variables, use the ``key`` keyword argument.
::

    >>> # only load MaNGA environment variables
    >>> my_tree = Tree(key='manga')

    >>> # load MaNGA and eBOSS
    >>> my_tree = Tree(key=['eboss', 'manga'])

The environment variables for the specified keys are now loaded into your Python ``os`` environment
::

    >>> import os
    >>> os.environ['MANGA_SPECTRO_REDUX']

You can load a new section into an existing tree with `.Tree.add_limbs`
::

    >>> # adds the APO tree section into your os environment
    >>> my_tree.add_limbs(key='apo')

To see what keys are available in the currently loaded ``Tree``, use `.Tree.list_keys`.
::

    >>> my_tree.list_keys()
    ['EBOSS', 'MANGA']


Dynamically switching configurations
------------------------------------

You can load a tree environment with a different configuration during instantiation.
::

    >>> my_tree = Tree(config='dr15')
    >>> my_tree
    Tree(sas_base_dir=/Users/Brian/Work/sdss/sas, config=dr15)

Instantiating a tree in this way will not overwrite any existing, or prior set, environment variables.  To
update existing tree environment variables after loading one configuration within the same session, you
can use `.Tree.replant_tree`
::

    >>> # load the default tree
    >>> my_tree = Tree()

    >>> # switch to the dr15 tree
    >>> my_tree.replant_tree(config='dr15')

If you wish to preserve your original os environment during a tree replanting, set ``preserve_envvars=True``.  This will preserve your
entire ``os.environ``.
::

    >>> # switch to the sdss5 tree, preserving your entire original os environment
    >>> my_tree.replant_tree('sdss5', preserve_envvars=True)

Alternatively, you can preserve only a subset of environment variables by passing in a list.
::

    >>> # switch to the sdss5 tree, preserving a single envvar
    >>> my_tree.replant_tree('sdss5', preserve_envvars=['ROBOSTRATEGY_DATA'])

If you wish to permanently preserve your locally set environment variables, you can set the ``preserve_envvars`` parameter to ``true`` in
a custom tree YAML configuration file located at ``~/.config/sdss/tree.yml``.  For example
::

    preserve_envvars: true

Alternatively, you can permanently set a subset of environment variables to preserve by defining a list.
::

    preserve_envvars:
      - ROBOSTRATEGY_DATA
      - ALLWISE_DIR


Accessing your original environment
-----------------------------------

To recover a copy of your original Python session ``os.environ``, use `.Tree.get_orig_os_environ`.
::

    >>> # get original os environ
    >>> orig = my_tree.get_orig_os_environ()

You can also reset the existing ``os.environ`` to its original state with `.Tree.reset_os_environ`.
::

    >>> # reset the os.environ
    >>> my_tree.reset_os_environ()

Seeing what's available
-----------------------

To see what environment configurations are available to load with `.Tree`, use the `.Tree.list_available_configs` method.
::

    >>> my_tree = Tree()
    >>> my_tree.list_available_configs()
    ['bosswork.cfg', 'dr7.cfg', 'dr8.cfg', 'dr9.cfg', 'dr10.cfg', 'dr11.cfg', 'dr12.cfg',
    'dr13.cfg', 'dr14.cfg', 'dr15.cfg', 'dr16.cfg', 'mpl9.cfg', 'sdss5.cfg', 'sdsswork.cfg']

To see the available data releases, use the `.Tree.get_available_releases` method.  This will return a list of
all public Data Release (DR) versions along with any internal survey release versions, e.g. MaNGA's MPLs.  Any config
files that end with ``work`` get combined into a single ``work`` release.
::

    >>> my_tree = Tree()
    >>> my_tree.get_available_releases()
    ['WORK', 'DR7', 'DR8', 'DR9', 'DR10', 'DR11', 'DR12', 'DR13', 'DR14', 'DR15', 'DR16']

    >>> # return only the public data releases
    >>> my_tree.get_available_releases(public=True)
    ['DR7', 'DR8', 'DR9', 'DR10', 'DR11', 'DR12', 'DR13', 'DR14', 'DR15', 'DR16']

To show the environments for all possible configurations, use `.Tree.show_forest`.  It returns a dictionary of all configurations
and their defined environment variables.
::

    >>> # get all possible environments
    >>> envs = my_tree.show_forest()
    >>> envs.keys()
    dict_keys(['bosswork', 'dr10', 'dr11', 'dr12', 'dr13', 'dr14', 'dr15', 'dr16', 'dr17', 'dr7',
    'dr8', 'dr9', 'mpl10', 'mpl3', 'mpl4', 'mpl5', 'mpl6', 'mpl7', 'mpl8', 'mpl9', 'sdss5', 'sdsswork'])

.. _tree-api:

Reference/API
-------------

.. rubric:: Class

.. autosummary:: tree.tree.Tree

.. rubric:: Methods

.. autosummary::

    tree.tree.Tree.add_limbs
    tree.tree.Tree.list_keys
    tree.tree.Tree.replant_tree
    tree.tree.Tree.get_orig_os_environ
    tree.tree.Tree.reset_os_environ
    tree.tree.Tree.list_available_configs
    tree.tree.Tree.get_available_releases
    tree.tree.Tree.show_forest
    tree.tree.Tree.set_product_root

