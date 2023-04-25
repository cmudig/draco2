from fastapi import FastAPI

import draco.server.routers as routers
from draco import Draco


class DracoAPI:
    """
    A class responsible for conveniently creating a FastAPI server
    exposing the capabilities of Draco. Provides sensible defaults
    while allowing for customization of the underlying FastAPI instance
    as well as the routers used to expose the Draco features in a granular way.
    """

    def __init__(
        self,
        draco: Draco = Draco(),
        app: FastAPI = FastAPI(),
        base_routers: list[routers.BaseDracoRouter] | None = None,
    ):
        """
        Creates a new :code:`DracoAPI` instance. If no parameters are passed in,
        the default configuration of :code:`Draco` and :code:`FastAPI` is used.

        The :code:`base_routers` parameter governs the routers which get registered
        to the :code:`FastAPI` instance, that is, they define the actual endpoints
        which will be available. Default routers get registered automatically:

        - :code:`DracoRouter` - exposes the core functionality of :code:`Draco`
        - :code:`ClingoRouter` - exposes the functionality of the Clingo solver
        - :code:`RendererRouter` - exposes renderer functionality
        - :code:`UtilityRouter` - exposes various utility endpoints

        If you wish to enable only a subset of these endpoints,
        you can pass in a list of routers to the :code:`base_routers` parameter.
        The routers will be registered in the order they appear in the list.
        Note that to avoid inconsistencies between the :code:`Draco` instance
        and the routers, you should declare a :code:`Draco` instance first,
        use it to construct your routers, then pass it into the constructor too.

        Let's suppose that you want to enable only :code:`DracoRouter`
        and :code:`UtilityRouter` and configure them to use custom prefix and tags:

        .. code-block:: python

        >>> from draco import Draco
        >>> from draco.server.routers import DracoRouter, UtilityRouter
        >>> from draco.server import DracoAPI
        >>> draco = Draco()
        >>> draco_router = DracoRouter(draco,
        >>>                            prefix='/my-draco',
        >>>                            tags=['My Draco Tag'])
        >>> utility_router = UtilityRouter(draco,
        >>>                                prefix='/my-utility',
        >>>                                tags=['My Utility Tag'])
        >>> my_base_routers = [draco_router, utility_router]
        >>> my_api = DracoAPI(draco=draco, base_routers=my_base_routers)

        You can use the very same method to add support
        for more endpoints by registering further routers.

        :param draco: The :code:`Draco` instance to use.
                      Use this instance to configure the Draco programs
                      such as constraints and weights.
        :param app: The :code:`FastAPI` instance to use.
                    Use this instance to configure the FastAPI server
                    according to your needs.
        :param base_routers: Routers to be used by the server,
                             defining the actual endpoints.
        """
        self.draco = draco
        self.app = app

        # Creating the base routers if none were passed in
        if base_routers is None:
            draco_router = routers.DracoRouter(draco)
            clingo_router = routers.ClingoRouter(draco)
            renderer_router = routers.RendererRouter(draco)
            utility_router = routers.UtilityRouter(draco)
            self.base_routers = [
                clingo_router,
                draco_router,
                renderer_router,
                utility_router,
            ]
        else:
            self.base_routers = base_routers

        # Make sure we have at least one router
        if len(self.base_routers) == 0:
            raise ValueError(
                "At least one `BaseDracoRouter` must be provided. "
                "Otherwise you can just use FastAPI directly."
            )

        # Actually register the routers
        for router in self.base_routers:
            router.register()
            self.app.include_router(router)
