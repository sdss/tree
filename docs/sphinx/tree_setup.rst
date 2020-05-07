
.. _setup:

Environment Setup of the Tree
=============================

This page describes the creation of the SDSS config environment files necessary for most SDSS software and filesystem
navigation on the Science Archive Server (SAS).  Running this script will setup the SDSS tree system
in your local shell environment, for use with an environment manager like `Modules <http://modules.sourceforge.net/>`_,
or straight with ``bash`` or ``tsch``.

.. note::

    If you are only interested in using the Tree Python package and having dynamic environments, you do not
    need to perform this step, and can safely ignore this page.

Checkout or Install the ``tree`` product
----------------------------------------

To setup the tree, you first must install or checkout the product.  You can either install it with ``pip`` or check out
the product from Github.

Pip Install
^^^^^^^^^^^
To install it with pip, run
::

    pip install -U sdss-tree

Installing `tree` this way will provide a shell script that you can run from anywhere as ``setup_tree.py``.

Git Clone
^^^^^^^^^

First clone the product from github.  Navigate to the ``bin`` directory
::

    git clone https://github.com/sdss/tree tree
    cd tree/bin/

Installing `tree` this way means you must run the script as ``python setup_tree.py``.


Run Setup
^^^^^^^^^

The main script to create environment files is ``setup_tree.py``.  See setup_tree :ref:`usage <usage>` for full
documentation of the command-line tool and its parameters.  To create corresponding
``module``, ``bash``, and ``tcsh`` configuration files, run

::

    python setup_tree.py -v

This will take all config files located in ``tree/data`` and create environment files inside a specified output
directory (see :ref:`custom-output`) which can then be sourced into your corresponding shell environment.  The
script uses the environment variables ``$SAS_BASE_DIR`` and ``$TREE_DIR`` when identifying and creating
environment files.  If it cannot find an existing ``TREE_DIR`` it will create one corresponding to the top
level directory of the git repo or python package.  If it cannot find an existing ``SAS_BASE_DIR`` it will
prompt you to create one.

ModuleFiles
-----------

If you are using the ``modules`` environment manager, this script attempts to copy the module files
located in the output directory into your local ``$MODULES_DIR``.  If no modules path is specified, the script
attempts to identify your modules directory by taking the first path directory found in the ``$MODULEPATH``
environment variable. To specify a custom or specific ``MODULES_DIR``, use the ``modulesdir`` keyword argument.
::

    python setup_tree.py -m '/my/custom/path/modules/'

It will copy all module files found in ``tree/etc`` and place them inside ``$MODULES_DIR/tree/``.  For example
the ``etc/dr14.module`` file would get copied to ``/my/custom/path/modules/tree/dr14``.  When multiple module paths
are found, it prompts the user to choose which paths to copy the new modules files into.  If an existing `tree` module
directory is found, it also prompts if the user wishes to overwrite existing files.  For example,
::

    >>> python setup_tree.py -v
    Multiple module paths found. Choose which module paths to use (e.g. "1,2") or hit enter for "all":
    1. /Users/Brian/Work/github_projects/modulefiles
    2. /Users/Brian/Work/sdss/repo/modulefiles
    3. /Users/Brian/Work/sdss/data/modulefiles
    4. /Users/Brian/Work/sdss/sdss_install/github/modulefiles
    5. /Users/Brian/Work/sdss/sdss_install/svn/modulefiles
    6. /usr/local/Modules/modulefiles

    # select "1" to copy the files to only the 1st module path found
    1
    /Users/Brian/Work/github_projects/modulefiles/tree already exists! Overwrite? (y/n)

    # select "y" to overwrite any existing files
    y
    Copying modules from etc/ into /Users/Brian/Work/github_projects/modulefiles/tree

Example Files
-------------

Example config files with created environment files.  The ``setup_tree`` command will create ``.sh``, ``.csh`` environment
files for ``bash``, ``tsch`` shells, and ``.module`` files for use with the ``modules`` environment manager.

.. raw:: html

    <table class="table striped" style="width: 80%">
        <thead>
        <tr>
            <th style="width: 20%">SDSS Config</th>
            <th style="width: 20%">Data Directory</th>
            <th style="width: 25%">Output Directory</th>
        </tr>
        </thead>
        <tbody>
        <tr class='active'>
            <td>dr14</td><td>dr14.cfg</td><td>dr14.module, dr14.sh dr14.csh</td>
        </tr>
        <tr class='active'>
            <td>sdsswork</td><td>sdsswork.cfg</td><td>sdsswork.module, sdsswork.sh sdsswork.csh</td>
        </tr>
    </table>

If you are using ``bash`` or ``tsch`` simply copy the relevant files to a location of your choice and source the environment
file you wish to load in your ``.bashrc`` or ``.cshrc`` file.

Using with modules
------------------

If you are using ``modules`` as an environment varibale, you can easily switch between different environment configurations.
Before you can utilize the new module files, you must make sure the directory where the new module files were copied can
be used by ``modules``.  You can set this with the ``module use`` command.  For example, if the directory containing the
``tree`` modules was ``/Work/sdss/repo/modulefiles``, then type
::

    module use /Work/sdss/repo/modulefiles

and the ``tree`` modules should now be available.  To list the available modules for ``tree``, use ``module avail``.
::

    >>> module avail tree
    ----------------------------------------------------------------- /Work/sdss/repo/modulefiles ------------------------------------------------------------------
    tree/bosswork  tree/dr7  tree/dr8  tree/dr9  tree/dr10  tree/dr11  tree/dr12  tree/dr13  tree/dr14  tree/dr15  tree/dr16  tree/sdss5  tree/sdsswork(default)


You can load a module with the ``module load`` or ``module switch`` command.
::

    # to load the latest working SDSS environmnt
    module load tree/sdsswork

    # to load the DR16 SDSS environment
    module load tree/dr16

.. _custom-output:

Custom Output Path
------------------

The default ouput directory for the environment files depends on whether the ``tree`` product was
`git cloned` or `pip-installed.`

.. raw:: html

    <table class="table striped" style="width: 80%">
        <thead>
        <tr>
            <th style="width: 20%">Install Method</th>
            <th style="width: 25%">Ouput Directory</th>
        </tr>
        </thead>
        <tbody>
        <tr class='active'>
            <td>git clone</td><td>$TREE_DIR/etc</td>
        </tr>
        <tr class='active'>
            <td>pip</td><td>~/.tree/environments</td>
        </tr>
    </table>

To control where `setup_tree` creates the environment files, specify the ``--path`` keyword argument.
::

    # specify a custom output path
    setup_tree.py -v -p /my_output/environment/configs/


Creating Environment Symlinks
=============================

To create the environment index pages, with symlinks to the Tree environment paths for the SAS, run

::

    python setup_tree.py -e

This will scrape through the tree datamodel directory inside your ``$SAS_BASE_DIR`` and create corresponding
symlinks to every path inside a master ``env`` directory located at the top level.  By default it creates
the `index` html page for the SAS.  To create links for the Science Archive Mirror (SAM),
use the ``mirror`` keyword argument.
::

    python setup_tree.py -e --mirror

To create environment symlinks for only a specific configuration, e.g. the DR14 environment, use the ``only``
keyword argument.
::

    python setup_tree.py -e -o dr14






