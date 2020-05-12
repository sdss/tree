
.. _install:

Installation
============

This describes the various installation methods for the SDSS tree product.

Pip
---

The tree product is now available as a Python package, and is pip-installable.  Simply do::

    pip install sdss-tree

or to upgrage::

    pip install --upgrade sdss-tree

Development
-----------
Clone the repo and run pip install::

    git clone https://github.com/sdss/tree
    cd tree
    pip install .[dev]

Or to run in editable mode in order to track changes from `git pulls`, run::

    pip install -e .[dev]

