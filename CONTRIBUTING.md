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

## Development with Docker

We provide a pre-configured [Docker](https://www.docker.com) environment for a better developer experience. You can
execute the following commands from a UNIX shell to start the development environment:

```shell
# Build the docker image
NB_USER="draco2" && \
docker build --build-arg NB_USER=${NB_USER} -t draco2-dev . && \
# Start a container with local volume mounting and port forwarding for
# [Jupyter Book, FastAPI, Jupyter, Pyodide Console, JupyterLite]
docker run -it --rm \
               -v $(pwd):/home/${NB_USER}/app \
               -p 5000:5000 \
               -p 8000:8000 \
               -p 8888:8888 \
               -p 9000:9000 \
               -p 9999:9999 \
               --name draco2-dev draco2-dev bash
```

As soon as you are inside the container's shell, you can execute `make` targets as you would from your local machine.
You can run `make test` to verify that everything is working as expected.

The services for which we reserved the ports are:

- Jupyter Book (Project Documentation): [http://localhost:5000](http://localhost:5000). Start it by `make book-serve`.
- FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs). Start it by `make serve`.
- Jupyter: [http://localhost:8888](http://localhost:8888). Start it by `make lab`.

You can open new shells inside the running container with `docker exec -it draco2-dev bash`. This way it is OK to run
the above-listed commands which 'block' your current shell session.

## Making a release

- After pulling the latest commits, run `poetry version patch/minor/major` to update the version number in
  `pyproject.toml`.
- Run `git commit -am "chore: bump version to $(poetry version -s)"` to commit the version bump and add a tag with
  `git tag "v$(poetry version -s)"`.
- Run `poetry build` to build the package.
- Configure the PyPI credentials with `poetry config pypi-token.pypi <token>`.
- Run `poetry publish -r testpypi` to publish the package to [TestPyPI](https://test.pypi.org/project/draco/).
- Run `poetry publish` to publish the package to [PyPI](https://pypi.org/project/draco/).
- Push the commits and tags with `git push && git push --tags`.
- Create a [release on GitHub](https://github.com/cmudig/draco2/releases) for the new version tag.

### Pyodide Distributions Release

The Pyodide distribution used for [Jupyter Lite](https://dig.cmu.edu/draco2/jupyterlite) and the
[Pyodide Console](https://dig.cmu.edu/draco2/jupyterlite/static/pyodide/console.html) will be automatically attached to
the GitHub release via `.github/workflows/build.yml#pin_distro`. To make the integration of Draco into web applications
easier we also publish the Pyodide distribution to NPM via `.github/workflows/build.yml#npm_publish`. The NPM package is
called [draco-pyodide](https://www.npmjs.com/package/draco-pyodide) and can be installed as any other NPM package.
