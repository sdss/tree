# tree

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-tree/badge/?version=latest)](https://sdss-tree.readthedocs.io/en/latest/?badge=latest)
[![Build Sphinx Documentation](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml)
[![Build and Test](https://github.com/sdss/tree/actions/workflows/build.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/sdss/tree/branch/master/graph/badge.svg)](https://codecov.io/gh/sdss/tree)

This product contains the definition(s) of the SDSS Science Archiver Server (SAS) filesystem environment tree(s).  It
sets up the SDSS environment configuration files for loading either via the [Modules Environment Manager](http://modules.sourceforge.net/) or dynamically with a ``tree.Tree`` python package.  Available environments are a SDSS "working" environment, i.e. ``sdsswork`` or any number of environments for public Data
Releases, i.e. ``dr16.cfg``.  See full documentation at http://sdss-tree.readthedocs.io/en/latest/.


## Developer Install

### Local Install

To install tree for development locally:

```
git clone https://github.com/sdss/tree
cd tree
python bin/copy_data.py
pip install -e ".[dev,docs]"
```

`python bin/copy_data.py` must be run ahead of any package install or builds with `python -m build` to ensure the config files are properly in place.

### Install at Utah

To install at Utah for use with modules,
```
git clone https://github.com/sdss/tree main
cd main
python bin/setup_tree.py -v
```
Replace `main` with the desired branch or tag name as needed. Also, see the instructions on the [Wiki](https://wiki.sdss.org/display/DATA/tree#tree-InstallationofthetreeproductatUtah)

### Install as a Dependency

To install as a Python package dedendency for software use, install the latest tag straight from PyPi:
```
pip install sdss-tree
```

## Build Sphinx Docs

Within the top level repo directory, run the `sdsstools` commands:
```
# build the Sphinx documentation
sdss docs.build

# open the docs locally in a browser
sdss docs.show
```
Documentation is automatically built and pushed to Read The Docs.

## Testing
Tests are created using `pytest`.  Navigate to the `tests` directory from the top level and run with `pytest`.
```
cd tests
pytest
```

## Creating Releases

New releases of `sdss-tree` are created automatically, and pushed to [PyPi](https://pypi.org/project/sdss-tree/), when new tags are pushed to Github.  See the [Create Release](.github/workflows/release.yml) Github Action and [Releases](https://github.com/sdss/tree/releases) for the list.

New tag names follow the Python semantic versioning syntax, i.e. `X.Y.Z`.


## Useful links

- GitHub: https://github.com/sdss/tree
- Documentation: https://sdss-tree.readthedocs.org
- Issues: https://github.com/sdss/tree/issues
