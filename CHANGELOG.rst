.. _tree-changelog:

==========
Change Log
==========

This document records the main changes to the tree code.

4.0.0 (2023-06-01)
------------------
- General refactor and cleanup of the tree configs
- Removes MaNGA internal mpl configs
- Removes bosswork and sdsswork configs
- Renames sdss5 config to sdsswork, making sdss5 the default work setup
- Module creation creates a sdss5 module symlink to sdsswork

3.1.7 (2023-05-31)
------------------
- Tag before package cleanup and refactor
- Adds some initial paths for LVM DRP
- Updates confSummmary config paths for sdsscore

3.1.6 (2023-03-27)
------------------
- Fixing dr18 mos target envvar bug to MOS_TARGET
- Adding SDSS_HIPS envvar and moc path to sdss5 config

3.1.5 (2023-03-01)
------------------
- Added new config for IPL-2
- Make ``sdsstool`` and ``sdss_access`` module dependencies optional in ``setup_tree``

3.1.4 (2022-11-29)
------------------
- Adding new config for IPL-1
- Updating many paths within sdss5.cfg

3.1.3 (2022-06-23)
------------------
- Add methods ``identify_envvar`` and ``identify_section`` to ``Tree`` class.

3.1.2 (2022-05-13)
------------------
- Includes updates and changes to sdss5 paths and envvars

3.1.1 (2021-12-05)
------------------
- Added missing MANGA_SPECTRA_TEMPLATES to dr15 config.

3.1.0 (2021-09-24)
------------------
- Updating tree config for dr17 VACs
- Added new Sphinx doc page for computing changes in the tree
- Adds ``release_date`` to tree configs for DR and MPLs.  Unreleased configs have ``release_date`` set to None.
- Adds new ``release_date`` property to ``Tree`` which returns the release date as a ``datetime.date`` object.
- Expanding ``Tree.list_available_configs`` to sort by "DR", "MPL" and "IPL".
- Deprecating ``Tree.list_configs`` in favor of ``Tree.list_available_configs``

3.0.7 (2020-03-05)
------------------
- Added method ``get_release_from_config`` to convert a given tree ``config_name`` into its release name.
- Added a new ``release`` attribute, accessible on a ``Tree`` instance.
- Fixing the mangarss path template with proper "wave" keyword arg, similar to mangacube
- Adding new tree config for MaNGA release MPL-11

3.0.6 (2020-11-11)
------------------
- Added dr17 release config
- Added tree_version to bin, expected by some old/existing IDL product tags
- Updated the path syntax for special functions to "@[function_name]|" to resolve issues with inclusion next to other characters
- Added new sdss5 paths for apogee
- Changed sdss5 paths for apogee from sdss4 to handle ``healpix`` grouping and simplified kwargs with special functions
- Updating the code to write out old sdss_paths.ini file.
- Added ``preserve_envvars`` options to ``replant_tree`` to preserve users original environment variables

3.0.5 (2020-07-17)
------------------
- Added MaNGA MPL-10 release config
- Added new paths for DR16+; VACs for APOGEE_JOKER

3.0.4 (2020-06-04)
------------------

- Added `phase` property to python `tree`.  Tracks phase of current 'sdsswork' environment.
- Modified module setup to create "default" symlink for lua modules
- Added `write_old_paths_inifile` method to generate a version of the old sdss_paths.ini file
- Adding new paths for DR16+; VACs for EBOSS_LSS, ATLAS, SPECTRO_LENSING, BOSS_QSO

3.0.3 (2020-05-29)
------------------

- Removed specific version requirement 1.0.0 for sdss_access in module setup

3.0.2 (2020-05-21)
------------------

- Added correct path for DR9 PHOTOSWEEPS
- Corrected APOGEE_ASTRONN path in DR16
- Added BCAM_DATA_2S to DR16

3.0.1 (2020-05-21)
------------------

- Added prereqs to tree module files for sdss_access/1.0.0 and sdsstools/0.1.7

3.0.0 (2020-05-07)
------------------

- Major changes to environment configuration files
- Incompatible with 2.x versions
- Implements versioning of DR config files and `sdss_access` paths
- Each config file now inherits from another config file using `base` keyword.
- Each DR config now only contains new or modified definitions for that DR.
- New configs for internal releases can now be created, e.g. mpl9.cfg.
- Explicit case is recognized for environment names and tree ini sections
- Deprecated and Removed sdss_paths.ini file
- New PATHS ini section in environment config files defines `sdss_access` paths
- Symbol for "special function" path definition has changed from `%` to `@`
- Refactored ``compute_changelog`` function to return dictionary and compute PATHS differences
- Added changelog compute functions ``compute_environment_changes``, and ``compute_path_changes``.
- Added changelog print functions ``print_environment``, and ``print_paths``.
- Moved tests out of ``tree`` python package to top level.
- Deprecated included logger and config in favor of ``sdsstools`` logger and config.
- Simplified python package setup.cfg and consolidated requirements files


2.15.10 (2020-04-13)
--------------------

Added
^^^^^
- new function ``compute_changelog`` to print difference between two tree environments
- new sphinx documentation on all DR tree environments and environment changes between DRs

Changed
^^^^^^^
- added wave keyword to mangacube/rss paths to handle LOG/LIN switch
- updated Tree python code to handle new cfg inheritance and versioning

2.15.9 (2020-03-16)
-------------------

Fixed
^^^^^
- standardized case output for ``get_available_releases`` method.  Added ``public`` only option.

2.15.8 (2020-03-15)
-------------------

Added
^^^^^
- new method ``list_available_configs`` that lists the available config files to load with Tree
- new method ``get_available_releases`` that builds a list of data releases from the config files

Fixed
^^^^^
- Issue :issue:`11` - silence and no input when multiple module paths found

2.15.7 (2019-12-06)
-------------------

Added
^^^^^
- new path definitions for MaNGA VAC Visual Morphology
- new path definition for MaNGA VAC Galaxy Zoo
- new path definitions for MaNGA VAC Firefly
- new path definitions for MaNGA VAC GEMA
- new documentation for adding new paths into sdss_paths.ini
- config file for DR16

Fixed
^^^^^
- Issue :issue:`10` - bug fix in setup_tree.py

2.15.6 (2019-07-26)
-------------------

Refactored
^^^^^^^^^^
- Modified data/cfg structure to handle versioning of envvar and path definitions
    - data cfg files now inherit from one another
    - deprecated sdss_paths.ini file and moved into new PATHS section in individual cfg files

Added
^^^^^
- new temporary path for manga images for releases MPL-8 and up
- new method show_forest to display the environment for configs not currently loaded
- new method list_configs to show all available configs for loading
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
