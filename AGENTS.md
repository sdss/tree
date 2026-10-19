---
description: "Python package for defining and setting up SDSS Science Archive Server filesystem environments, usable through Environment Modules or the tree Python API."
---

# Repository Guide

## Package Contents

- `src/tree/` contains the Python package, including tree configuration handling, changelog support, bundled environment configuration files, and package data.
- `bin/` contains setup utilities for installing the tree environment.
- `docs/` contains the Sphinx documentation.
- `tests/` contains the pytest suite and its fixtures.
- `pyproject.toml` defines package metadata, dependencies, and tool configuration.

## Environment and Installation

Use `uv` for development. Before running commands, check for an existing `.venv` in the repository root. Use that environment if it exists; otherwise create it with `uv venv`. Then install the package and all development, test, and documentation dependencies:

```bash
uv sync --all-groups
```

`uv run` automatically uses the project environment, so activation is not required.

## Tests

Run the full test suite from the repository root:

```bash
uv run pytest
```

## Formatting and Linting

Use Ruff to format the code and check for lint issues:

```bash
uv run ruff format .
uv run ruff check .
```