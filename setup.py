#!/usr/bin/env python

from draco import __version__


setup(
    name="draco",
    version=__version__,
    description="Visualization recommendation using constraints",
    long_description=long_description,
    author="Dominik Moritz, Chenglong Wang",
    author_email="domoritz@cs.washington.edu, clwang@cs.washington.edu",
    license="BSD-3",
    url="https://github.com/cmudig/draco2",
    packages=["draco"],
    entry_points={"console_scripts": ["draco=draco.cli:main"]},
    install_requires=["clyngor"],
    include_package_data=True,
    extras_require={
        "test": ["coverage", "pytest", "pytest-cov", "black", "ansunit", "mypy"]
    },
    package_data={
        "draco": [
            "../asp/*.lp",
            "../js/bin/*",
            "../js/build/draco.js*",
            "../LICENSE",
            "../README.md",
        ]
    },
    # cmdclass={"test": RunTests},
)
