# Introduction

In this book, we describe a new version of Draco. Draco was first published in {cite}`moritz2018formalizing`.

Draco has three parts.

1. A general description language for visualizations as facts.
   [Learn more about how Draco describes visualizations.](facts/intro.md)
2. A knowledge base as constraints over facts. This knowledge base describes which visualizations are valid and what
   visualizations might be preferred.
3. An API to use the [Clingo](https://potassco.org/clingo/) solver to apply the knowledge base to visualizations
   described as a set of facts. [Go to the API docs.](api/intro.md)

The code for Draco is [available as open source on GitHub](https://github.com/cmudig/draco2).

## Installation

You can install the Draco package from Pypi via `pip install draco --pre`. Note that the new version of Draco is current
a prerelease.
