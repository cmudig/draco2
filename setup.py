#!/usr/bin/env python

from codecs import open
from os.path import abspath, dirname, join

from setuptools import setup

from draco import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="draco",
    version=__version__,
    description="Visualization recommendation using constraints",
    long_description=long_description,
    author="Dominik Moritz, Chenglong Wang",
    author_email="domoritz@cs.washington.edu, clwang@cs.washington.edu",
    license="MIT",
    url="https://github.com/cmudig/draco2",
    packages=["draco"],
    include_package_data=True,
    install_requires=["clingo", "pandas"],
    package_data={
        "draco": [
            "../LICENSE",
            "../README.md",
        ]
    },
)
