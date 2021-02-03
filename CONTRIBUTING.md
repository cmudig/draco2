# Contributing to Draco

We welcome any input, feedback, bug reports, and contributions via [Draco's GitHub Repository](https://github.com/cmudig/draco2).

This document describes how you can set up your development environment if you want to contribute to the code.

## Development setup

This project uses [Poetry](https://python-poetry.org). Please skim the documentation if you are not familiar with Poetry.

After installing the dependencies with `poetry install`, you can activate the virtual environment with `poetry shell`.

## Development setup with Conda

You can set up this project with Poetry inside a Conda environment.

Install Conda (we use [miniforge](https://github.com/conda-forge/miniforge) but any other conda distribution should work as well).

To create a virtual environment named `draco`, you can run

```sh
conda create -n draco python=3.9
conda activate draco
poetry install
```

Next time you want to work on Draco, you can just run `conda activate draco`.

## Make commands

You can run various test and lint commands via make. For example, run `make test` to run the tests. Or just `make` to run tests, lint, and type checks.
