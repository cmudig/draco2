import draco.server.models.renderer as endpoint_models
import draco.server.services.renderer as service

from .base import BaseDracoRouter


class RendererRouter(BaseDracoRouter):
    """Router exposing renderer functionality through REST endpoints."""

    __DEFAULT_PREFIX__ = "/renderer"
    __DEFAULT_TAGS__ = ["Renderer"]

    def __init__(self, draco, **kwargs):
        c = RendererRouter
        super().__init__(
            draco,
            prefix=kwargs.pop("prefix", c.__DEFAULT_PREFIX__),
            tags=kwargs.pop("tags", c.__DEFAULT_TAGS__),
            **kwargs
        )

    @staticmethod
    def _register(router: "BaseDracoRouter") -> None:
        @router.post("/render-spec")
        def render_spec(
            dto: endpoint_models.RenderSpecDTO,
        ) -> endpoint_models.RenderSpecReturn:
            return service.render_spec(spec=dto.spec)
