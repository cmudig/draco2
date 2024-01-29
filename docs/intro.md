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

If you use Draco, please cite our [award winning](https://ieeevis.org/year/2023/info/awards/best-paper-awards)
[paper](https://arxiv.org/abs/2308.14247):

```bibtex
@misc{draco2,
   Author = {Junran Yang and Péter Ferenc Gyarmati and Zehua Zeng and Dominik Moritz},
   Title = {Draco 2: An Extensible Platform to Model Visualization Design},
   Year = {2023},
   Organization = {{IEEE}},
   Eprint = {arXiv:2308.14247},
   Journal = {Proceedings of the 2023 {IEEE} Conference on Visualizations (VIS)},
}
```

## Installation

You can install the Draco package from [PyPI](https://pypi.org/project/draco/) via `pip install draco`.
