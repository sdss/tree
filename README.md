# sdss-tree

![Versions](https://img.shields.io/badge/python->=3.11-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-tree/badge/?version=latest)](https://sdss-tree.readthedocs.io/en/latest/?badge=latest)
[![Build Sphinx Documentation](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/sphinxbuild.yml)
[![Build and Test](https://github.com/sdss/tree/actions/workflows/build.yml/badge.svg)](https://github.com/sdss/tree/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/sdss/tree/branch/master/graph/badge.svg)](https://codecov.io/gh/sdss/tree)

This product contains the definition(s) of the SDSS Science Archiver Server (SAS) filesystem environment tree(s).  It
sets up the SDSS environment configuration files for loading either via the [Modules Environment Manager](http://modules.sourceforge.net/) or dynamically with a ``tree.Tree`` python package.  Available environments are a SDSS "working" environment, i.e. ``sdsswork`` or any number of environments for public Data
Releases, i.e. ``dr16.cfg``.  See full documentation at http://sdss-tree.readthedocs.io/en/latest/.


## Developer Install

### Local Install

Install [uv](https://docs.astral.sh/uv/), then clone the repository and sync its dependencies:

```bash
git clone https://github.com/sdss/tree
cd tree
uv sync --all-groups
```

This creates a local `.venv`, installs the checkout in editable mode, and installs the development, test, and documentation dependencies. The configuration files are packaged from `src/tree/data`; the top-level `data/` symlink remains for legacy checkout usage.

### Install at Utah

To install at Utah for use with modules,

```bash
git clone https://github.com/sdss/tree main
cd main
uv sync
uv run python bin/setup_tree.py -v
```

Replace `main` with the desired branch or tag name as needed. Also, see the instructions on the [Wiki](https://wiki.sdss.org/display/DATA/tree#tree-InstallationofthetreeproductatUtah)

### Install as a Dependency

To add the latest PyPI release to a project managed by uv:

```bash
uv add sdss-tree
```

## Documentation

Install the documentation dependencies and run the live Nox session from the repository root:

```bash
uv sync --group docs
uv run nox -s docs-live
```

This starts `sphinx-autobuild`, opens the documentation in a browser, and rebuilds it as source files change.

Documentation is automatically built and pushed to Read The Docs.

## Testing

Run the test suite from the repository root with:

```bash
uv run pytest
```

## Creating Releases

New releases of `sdss-tree` are created automatically, and pushed to [PyPi](https://pypi.org/project/sdss-tree/), when new tags are pushed to Github.  See the [Create Release](.github/workflows/release.yml) Github Action and [Releases](https://github.com/sdss/tree/releases) for the list.

New tag names follow the Python semantic versioning syntax, i.e. `X.Y.Z`.


## Useful links

- GitHub: https://github.com/sdss/tree
- Documentation: https://sdss-tree.readthedocs.org
- Issues: https://github.com/sdss/tree/issues
