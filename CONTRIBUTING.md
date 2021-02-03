# Contributing to Draco

We welcome any input, feedback, bug reports, and contributions via [Draco's GitHub Repository](https://github.com/cmudig/draco2).

This document describes how you can set up your development environment if you want to contribute to the code.

## Development setup

Install conda (we use [miniforge](https://github.com/conda-forge/miniforge) but any other conda distribution should work as well).

To create the virtual environment `draco`, you can run

```sh
conda env create -f environment.yml
conda activate draco
python setup.py develop
```

To update the environment when dependencies have changed, run

```sh
conda env update -f environment.yml
```

## Updating the dependencies

If you update or add a dependency, update update the environment file `environment.yml` and `pyproject.toml` and then update your environment from the environment file.

## Make commands

You can run various test and lint commands via make. For example, run `make test` to run the tests. Or just `make` to run tests, lint, and type checks.
