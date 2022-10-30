<!-- #region -->

# Server

The server module has two main components: the [BaseDracoRouter](#basedracorouter) abstract base class to provide a
template for declaring groups of API endpoints which might use a [Draco](./draco.ipynb) instance under the hood and the
[DracoAPI](#dracoapi) class to handle registering the actual endpoints to a [FastAPI](https://fastapi.tiangolo.com/)
instance and to allow for customization of the API.

You can learn more on applications of the server module in the [applications](../applications/server.md) section which
includes examples.

## `BaseDracoRouter`

```{eval-rst}
.. autoclass:: draco.server.BaseDracoRouter
  :members:

  .. automethod:: __init__
```

```{note}
This abstract class has three concrete implementations:

- [ClingoRouter](#clingorouter)
- [DracoRouter](#dracorouter)
- [UtilityRouter](#utilityrouter)
```

### `ClingoRouter`

```{note}
Defines endpoints under `/clingo`.
```

```{eval-rst}
.. autoclass:: draco.server.routers.ClingoRouter
  :show-inheritance:
  :members:

  .. automethod:: __init__
```

### `DracoRouter`

```{note}
Defines endpoints under `/draco`.
```

```{eval-rst}
.. autoclass:: draco.server.routers.DracoRouter
  :show-inheritance:
  :members:

  .. automethod:: __init__
```

### `UtilityRouter`

```{note}
Defines endpoints under `/utility`.
```

```{eval-rst}
.. autoclass:: draco.server.routers.UtilityRouter
  :show-inheritance:
  :members:

  .. automethod:: __init__
```

## `DracoAPI`

```{eval-rst}
.. autoclass:: draco.server.DracoAPI
  :members:

  .. automethod:: __init__
```

<!-- #endregion -->
