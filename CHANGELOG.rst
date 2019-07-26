.. _tree-changelog:

==========
Change Log
==========

This document records the main changes to the tree code.

2.15.7 (unreleased)
-------------------

2.15.6 (2019-07-26)
-------------------

Added
^^^^^
- new temporary path for manga images for releases MPL-8 and up
- new tests for setting up the tree; creating and copying module/bash files and env symlinks
- added the option for env symlink creation into the setup_tree.py bin file
- added option to specify default config to write into .version file

Changed
^^^^^^^
- replaced non-existent %designdir special function with %definitiondir 
- changed yaml loaded to use yaml.FullLoader in compliance with pyyaml 5.1
- switching disutils.StrictVersion to more standard parse_version

Fixed
^^^^^
- Broken syntax on apogee in paths.ini file
- Broken syntax in some platelist definitions
- Broken etc/Makefile after implementation of new setup_tree.py
- Bugfix on setup_tree.py when empty tree directory first entry in MODULEPATH

2.15.5 (2018-09-06)
-------------------

Changed
^^^^^^^
* Refactored bin/setup_tree to install module files


2.15.4 (2018-07-09)
-------------------

Changed
^^^^^^^
* Wrapped config file opens in with to ensure proper file closure

Fixed
^^^^^
* Bug when config=None is explicitly passed into Tree


2.15.3 (2017-12-02)
-------------------

Added
^^^^^
* method to list_keys
* ability to load different config files
* ability to load a new section of the tree in an existing environment
* new documentation
* new sphinx plugin to auto document the tree config

Changed
^^^^^^^
* Moved camelCase methods to underscore methods

2.15.2 (2017-11-29)
-------------------

Added
^^^^^
* Synced a bunch of new config changes from svn that were forgotten.


2.15.1 (2017-11-29)
-------------------

Changed
^^^^^^^
* Added Tree import in init for easier imports from top level

2.15.0 (2017-11-29)
---------------------

Fixed
^^^^^
* Fixed setup to include data files
* Updated versioning to sync with svn tags

.. _changelog-0.1.0:
0.1.0 (2017-11-29)
------------------

Added
^^^^^
* Created new tree python product using the cookiecutter template
* A python form of Tree to load SDSS environments
