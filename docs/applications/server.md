# Server

If you want to use Draco in an environment other than Python, you can access its capabilities through a dedicated REST
API, built with [FastAPI](https://fastapi.tiangolo.com/).

## Starting the Server

Based on your needs, you can start the server directly from the command line or as a standalone Python program.

- For simpler use cases such as general exploration of the project or making use of the default Draco model we recommend
  starting the server from the [command line](#command-line-interface)
- For more complex use cases such as customizing Draco's model or extending the API routes, you can start a custom
  server instance as a [standalone Python program](#standalone-python-program)

### Command Line Interface

You can start a default instance of the server without passing any arguments:

```shell
python -m draco.server
```

A comprehensive OpenAPI documentation of the API will be available at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), also allowing for sending requests directly from the browser
to get a better idea of how the API works.

You can access the CLI options by executing `python -m draco.server --help`.

```text
usage: python -m draco.server [options]

FastAPI Server exposing the capabilities of Draco

options:
  -h, --help   show this help message and exit
  --host HOST  Host to run server on. Defaults to 127.0.0.1
  --port PORT  Port to run server on. Defaults to 8000
  --reload     Enable auto-reloading of the server on code changes.
```

_Please note that the `--reload` option is only relevant for local server development._

### Standalone Python Program

The main purpose of Draco's server component is to provide a **minimal** REST API to be able to use it in a
client-agnostic way. That being said, there is a good chance that the core server does not fit **all** your needs. While
we focused on simplicity we also did not want to compromise on extensibility. That is why we implemented the server to
be fully compatible with [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/).

Before diving into creating a custom Draco server it might be useful to familiarize yourself with the
[module's API](../api/server.md).

Please note that for all the following examples we assume that you have already installed Draco and its dependencies.

#### Minimal Example

##### Via Quick Command

Create a Python file called `my_server.py` and add the following code:

```python
# my_server.py
from draco.server import DracoAPI

draco_api = DracoAPI()
```

Run by executing the following command:

```shell
uvicorn my_server:draco_api.app --reload
```

```{note}
The command `uvicorn my_server:my_app --reload` refers to:

- `my_server`: the file `my_server.py` (the Python "module").
- `draco_api.app`: the internal `FastAPI` app of the `draco_api` instance, declared with the line `draco_api = DracoAPI()`.
- `--reload`: make the server restart after code changes. Only use for development.
```

##### Via `__main__`

The example below demonstrates how to spin up a server instance using a Python module as `__main__` using `uvicorn`.
This might be useful if you would like to programmatically set server configurations such as host, port, workers, etc.

Create a Python file called `my_server.py` and add the following code:

```python
# my_server.py
from draco.server import DracoAPI
import uvicorn

draco_api = DracoAPI()

if __name__ == '__main__':
    uvicorn.run("my_server:draco_api.app", host='127.0.0.1', port=8000, reload=True)
```

#### Customizing Existing Routes

If you are satisfied with the functionality of the existing routes but would like to customize their metadata (endpoint
name, OpenAPI tags, etc.), you can do so by creating custom instances of our `BaseDracoRouter` implementations. The core
routers listed below.

- [`ClingoRouter`](../api/server.html#clingorouter): exposes capabilities of the [Clingo](https://potassco.org/clingo/)
  solver
- [`DracoRouter`](../api/server.html#dracorouter): exposes capabilities of the injected [Draco](../api/draco.ipynb)
  instance
- [`UtilityRouter`](../api/server.html#utilityrouter): exposes functions to convert between different response formats

The example below demonstrates how you can modify the endpoint prefix and OpenAPI tags of core routers.

```python
# my_server.py
from draco import Draco
from draco.server.routers import DracoRouter, UtilityRouter
from draco.server import DracoAPI

draco = Draco()
draco_router = DracoRouter(draco,
                           prefix='/my-draco',
                           tags=['My Draco Tag'])
utility_router = UtilityRouter(draco,
                               prefix='/my-utility',
                               tags=['My Utility Tag'])
my_base_routers = [draco_router, utility_router]
my_api = DracoAPI(draco=draco, base_routers=my_base_routers)
```

You can run the server using the following command:

```shell
uvicorn my_server:my_api.app
```

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to see the updated endpoint names and tags.

```{warning}
Since we did not import the `ClingoRouter` and passed it into the `my_base_routers` list in the example above,
the `/clingo` endpoint will not be available. However, you can import it and add a default instance of it
to the list if you wish to do so.
```

#### Adding New Routes

As `DracoAPI` makes heavy use of `FastAPI`, all its rules for adding new routes apply to `DracoAPI` as well. You can
familiarize yourself with the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/bigger-applications/) to
learn more about how to add new routes the "FastAPI way".

In this example we are focusing on adding a new route by creating a custom `BaseDracoRouter` implementation. The code
below is the implementation of an extremely simple endpoint, available at `/metadata/doc` which will return the module
documentation of the used `Draco` instance.

Create a Python file called `my_server.py` and add the following code:

```python
# my_server.py
import pydantic

import draco.server.routers as routers
from draco import Draco
from draco.server import DracoAPI


class DracoDocReturn(pydantic.BaseModel):
    """Pydantic model for our custom endpoint."""

    content: str


class DracoMetadataRouter(routers.BaseDracoRouter):
    @staticmethod
    def _register(router: routers.BaseDracoRouter):
        """
        Method for registering the endpoints.

        We are using a static method here,
        since we expect the endpoint structure to be the same
        for all instances of this router,
        hence we are defining it in a class-scoped method.

        However, we are not expecting that each router will use the
        same dependencies, therefore we are passing a pre-configured `router` instance
        as a parameter to this method, allowing us to use it to register the endpoints
        while being able to transparently use its custom dependencies, such as
        a customized `Draco` instance.
        """

        @router.get("/doc")
        def draco_doc() -> DracoDocReturn:
            # Note that we can access the server's Draco instance through the router
            return DracoDocReturn(content=router.draco.__doc__)


# This instance might be customized via constructor params
my_draco = Draco()

# the core routers provided by `draco.server`, configured with the `my_draco` instance
core_routers = [
    routers.ClingoRouter(my_draco),
    routers.DracoRouter(my_draco),
    routers.UtilityRouter(my_draco),
]

# our custom router, configured with the `my_draco` instance
custom_routers = [DracoMetadataRouter(my_draco, prefix="/metadata", tags=["Metadata"])]

# a list of all routers to be used by the server which inherit from `BaseDracoRouter`
base_routers = core_routers + custom_routers

# Constructing our server instance with the custom routers
my_api = DracoAPI(draco=my_draco, base_routers=base_routers)
```

You can run the server using the following command:

```shell
uvicorn my_server:my_api.app
```

Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to see the custom endpoint `/metadata/doc` tagged
with `Metadata` as well as the core endpoints.

## Further Customization

As the examples above demonstrate, `DracoAPI` is highly customizable and extensible, allowing for treating routers as
building blocks for your own custom server implementation. If the examples here are not enough to satisfy your needs,
you can always take a look at the capabilities of the underlying [FastAPI](https://fastapi.tiangolo.com/) framework.

If you have suggestions more specific to `Draco` or `DracoAPI`, feel free to
[open an issue](https://github.com/cmudig/draco2/issues/new/choose) for it.
