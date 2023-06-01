# tree

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-tree/badge/?version=latest)](https://sdss-tree.readthedocs.io/en/latest/?badge=latest)
[![Build Sphinx Documentation](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml)
[![Build and Test](https://github.com/sdss/tree/actions/workflows/build.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/sdss/tree/branch/master/graph/badge.svg)](https://codecov.io/gh/sdss/tree)
[![Coveralls](https://coveralls.io/repos/github/sdss/tree/badge.svg)](https://coveralls.io/github/sdss/tree)

This product contains the definition(s) of the SDSS Science Archiver Server (SAS) filesystem environment tree(s).  It
sets up the SDSS environment configuration files for loading either via the [Modules Environment Manager](http://modules.sourceforge.net/) or dynamically with a ``tree.Tree`` python package.  Available environments are a SDSS "working" environment, i.e. ``sdsswork`` or any number of environments for public Data
Releases, i.e. ``dr16.cfg``.  See full documentation at http://sdss-tree.readthedocs.io/en/latest/.


## Developer Install

To install tree for development:

```
git clone https://github.com/sdss/tree
cd tree
pip install -e ".[dev,docs]"
```

## Build Sphinx Docs

Within the top level repo directory, run the `sdsstools` commands:
```
# build the Sphinx documentation
sdss docs.build

# open the docs locally in a browser
sdss docs.show
```

## Testing
Tests are created using `pytest`.  Navigate to the `tests` directory from the top level and run with `pytest`.
```
cd tests
pytest
```

## Creating Releases

New releases of `sdss-tree` are created automatically when new tags are pushed to Github.  See the [Create Release](.github/workflows/release.yml) Github Action and [Releases](https://github.com/sdss/tree/releases) for the list.


## Useful links

- GitHub: https://github.com/sdss/tree
- Documentation: https://sdss-tree.readthedocs.org
- Issues: https://github.com/sdss/tree/issues



