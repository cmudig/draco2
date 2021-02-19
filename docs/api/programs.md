# Programs

Draco exposes the following programs.

- `definitions`
- `constraints`
- `generate`
- `hard`
- `helpers`

Draco loads these programs from files.

## Options for Each Program

```{eval-rst}
.. autodata:: draco.programs
   :annotation:
```

Each program has both the program as well as the program as a dictionary of blocks. Blocks allow you to pick and choose parts of a program and access documentation.

```{eval-rst}
.. autoclass:: draco.programs.Program
.. autoclass:: draco.asp_utils.Blocks
.. autoclass:: draco.asp_utils.Block
```
