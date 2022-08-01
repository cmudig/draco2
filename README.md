<p align="center">
   <a href="https://github.com/cmudig/draco2">
      <picture>
         <source media="(prefers-color-scheme: dark)" srcset="https://github.com/cmudig/draco2/raw/main/docs/logo-light.png">
         <source media="(prefers-color-scheme: light)" srcset="https://github.com/cmudig/draco2/raw/main/docs/logo-dark.png">
         <img alt="The Draco logo. A set of circles connected by lines depicting the draco star constellation." src="https://github.com/cmudig/draco2/raw/main/docs/logo-light.png" width=260>
      </picture>
   </a>
</p>

# Draco v2

[![Test](https://github.com/cmudig/draco2/actions/workflows/test.yml/badge.svg)](https://github.com/cmudig/draco2/actions/workflows/test.yml)
[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/cmudig/draco2/branch/main/graph/badge.svg)](https://codecov.io/gh/cmudig/draco2)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cmudig/draco2.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cmudig/draco2/context:python)

**Work in Progress**

Draco is a formal framework for representing design knowledge about effective visualization design as a collection of constraints. You can use Draco to find effective visualization visual designs or validate visualization designs. Draco's constraints are implemented in based on Answer Set Programming (ASP) and solved with the Clingo constraint solver. We also implemented a way to learn weights for the recommendation system directly from the results of graphical perception experiment. Draco v2 is a much imprived version of the first iteration of [Draco](https://github.com/uwdata/draco).

## Documentation

Read about Draco in the online book at https://dig.cmu.edu/draco2/. In the documentation, we just refer to _Draco_ without a version.

## What's different from [Draco v1](https://github.com/uwdata/draco)?

- Draco v2 is completely written in Python. No more need to run both Python and Node. We still use ASP for the knowledge base.
- Generalized and extended chart specification format. The new format is more extensible with custom properties.
- Suport for multiple views and view compostion.
- High test-coverage, documentation, and updated development tooling.

## Contributing

We welcome any input, feedback, bug reports, and contributions. You can learn about setting up your development environment in [CONTRIBUTING.md](https://github.com/cmudig/draco2/blob/main/CONTRIBUTING.md).
