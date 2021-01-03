# Draco v2
![Test](https://github.com/cmudig/draco2/workflows/Test/badge.svg)
[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Work in Progress**

Experimental/modular version of [Draco](https://github.com/uwdata/draco).

## Install

TODO

## Development setup

Install conda (we use [miniforge](https://github.com/conda-forge/miniforge) but any other conda distribution should work as well).

To create the virtual environment `draco`, you can run

```sh
conda env create -f environment.yml
conda activate draco
```

To update the environment when dependencies have changed, run

```sh
conda env update -f environment.yml --prune
```

This command will ensure that you have the exact same dependencies as other developers.

## Updating the dependencies

To add a new dependency or update a dependency, update `requirements.txt` or `requirements-dev.txt`. Then update the environment.

```sh
conda install --file requirements.txt --file requirements-dev.txt
```

You can update the dependencies in your environment with

```sh
conda update --all
```

If you make changes to the environments, make sure to update the `environment.yml` file that we use to share dependency versions.

```sh
conda env export | grep -v "^prefix: " > environment.yml
```
