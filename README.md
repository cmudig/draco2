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
```

To update the environment when dependencies have changed

```sh
conda env update -f environment.yml
```

## Update the environment

After adding a new dependency or updating a dependency, you need to update the environment as well.
