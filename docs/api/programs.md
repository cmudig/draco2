<!-- #region -->

# Programs

Draco loads its programs from the [asp](https://github.com/cmudig/draco2/tree/main/draco/asp) directory that contains
the Draco knowledge base as answer set programs. Draco exposes the following programs.

- `definitions`: loads from [`define.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/define.lp) that declares
  the domains to visualization attributes.
- `constraints`: loads from [`constraints.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/constraints.lp) that
  restricts the search space to follow the correct draco general description language.
- `generate`: loads from [`generate.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/generate.lp) that sets up
  the search space.
- `hard`: loads from [`hard.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/hard.lp) that restricts the search
  space to only well-formed and expressive specifications.
- `helpers`: loads from [`helpers.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/helpers.lp) that defines
  useful helper functions.

Additionally, the asp directory contains a [`soft.lp`](https://github.com/cmudig/draco2/blob/main/draco/asp/soft.lp)
that defines soft constraints in the form of violation/1 and violation/2 predicates. By themselves, these predicates
don't change the search.

## Options for Each Program

```{eval-rst}
.. autodata:: draco.programs
   :annotation:
```

Each program has both the program as well as the program as a dictionary of blocks. Blocks allow you to pick and choose
parts of a program and access documentation.

```{eval-rst}
.. autoclass:: draco.programs.Program
.. autoclass:: draco.asp_utils.Blocks
.. autoclass:: draco.asp_utils.Block
```

<!-- #endregion -->
