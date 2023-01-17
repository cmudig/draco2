<!-- #region -->

# Renderer

The renderer was designed with extensibility in mind and allows you to create custom renderers for different
specification formats. The renderer module exposes a [BaseRenderer](#baserenderer) abstract class to provide the clients
with a common interface. The [AltairRenderer](#altairrenderer) class is a concrete implementation of the
[BaseRenderer](#baserenderer). In order to constraint the input handled by [AltairRenderer](#altairrenderer), strict
typing is introduced in the [draco.renderer.altair.types](#types) module.

## `BaseRenderer`

```{eval-rst}
.. autoclass:: draco.renderer.BaseRenderer
  :members:

  .. automethod:: __init__
```

## `AltairRenderer`

```{eval-rst}
.. autoclass:: draco.renderer.AltairRenderer
  :members:

  .. automethod:: __init__
```

### Types

```{note}
Introducing the types through the below-described members made it possible to traverse specifications in a type-safe
manner in the [AltairRenderer](#altairrenderer) class. The types reflect the default specification form, as described
in the [Facts](../facts/intro) chapters.
```

```{eval-rst}
.. automodule:: draco.renderer.altair.types
    :members:
```

<!-- #endregion -->
