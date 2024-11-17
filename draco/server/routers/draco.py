import draco.server.models.draco as endpoint_models

from ..services.draco import DracoService
from .base import BaseDracoRouter


class DracoRouter(BaseDracoRouter):
    """Router exposing core functionality of :code:`Draco` through REST endpoints."""

    __DEFAULT_PREFIX__ = "/draco"
    __DEFAULT_TAGS__ = ["Draco"]

    def __init__(self, draco, **kwargs):
        c = DracoRouter
        super().__init__(
            draco,
            prefix=kwargs.pop("prefix", c.__DEFAULT_PREFIX__),
            tags=kwargs.pop("tags", c.__DEFAULT_TAGS__),
            **kwargs,
        )

    @staticmethod
    def _register(router: "BaseDracoRouter") -> None:
        service = DracoService(router.draco)

        @router.post("/check-spec")
        def check_spec(
            dto: endpoint_models.CheckSpecDTO,
        ) -> endpoint_models.CheckSpecReturn:
            return service.check_spec(dto.spec)  # pragma: no cover

        @router.post("/complete-spec")
        def complete_spec(
            dto: endpoint_models.CompleteSpecDTO,
        ) -> endpoint_models.CompleteSpecReturn:
            return service.complete_spec(dto.spec, dto.models)  # pragma: no cover

        @router.post("/count-preferences")
        def count_preferences(
            dto: endpoint_models.CountPreferencesDTO,
        ) -> endpoint_models.CountPreferencesReturn:
            return service.count_preferences(dto.spec)  # pragma: no cover

        @router.post("/get-violations")
        def get_violations(
            dto: endpoint_models.GetViolationsDTO,
        ) -> endpoint_models.GetViolationsReturn:
            return service.get_violations(dto.spec)  # pragma: no cover
