# Contributing to Draco

We welcome any input, feedback, bug reports, and contributions via
[Draco's GitHub Repository](https://github.com/cmudig/draco2).

This document describes how you can set up your development environment if you want to contribute to the code.

## Development setup

This project uses [Poetry](https://python-poetry.org). Please skim the documentation if you are not familiar with
Poetry.

After installing the dependencies with `poetry install`, you can activate the virtual environment with `poetry shell`.

## Development setup with Conda

You can set up this project with Poetry inside a Conda environment. Running inside a Conda environment can be useful to
install difficult to install native dependencies (like numpy). You can install any dependencies that are stubborn before
running `poetry install`.

Install Conda (we use [miniforge](https://github.com/conda-forge/miniforge) but any other Conda distribution should work
as well).

To create a virtual environment named `draco`, you can run

```sh
conda create -n draco python=3.10
conda activate draco
poetry install
```

Next time you want to work on Draco, you can just run `conda activate draco`.

## Install the pre-commit hooks

Install [pre-commit](https://pre-commit.com) and then install the hooks with `pre-commit install`. These hooks will
automatically format code before making a new commit.

## Make commands

You can run various test and lint commands via [`make`](https://www.gnu.org/software/make/). For example, run
`make test` to run the tests. Or just `make` to run tests, lint, and type checks.

## Update dependencies

Run `poetry show -o` to show the latest versions of the packages Draco depends on. Then update the dependencies
accordingly.

Run `poetry update` to update dependencies within the specified range and update the lockfile.

## Writing constraints

For more information about writing constraints and optimization-based problems, take a look at the
[Pottasco guide](https://github.com/potassco/guide/releases/).

## Server Development

You can start the custom [FastAPI](https://fastapi.tiangolo.com/) server in hot-reload mode with `make serve`. This way,
you can make changes to the server code and see the changes immediately. You can explore the API by visiting the OpenAPI
docs at [http://localhost:8000/docs](http://localhost:8000/docs).
