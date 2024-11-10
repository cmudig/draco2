import draco.server.models.clingo as endpoint_models
import draco.server.services.clingo as service

from .base import BaseDracoRouter


class ClingoRouter(BaseDracoRouter):
    """
    Router exposing `Clingo <https://potassco.org/clingo/>`_
    functionality through REST endpoints.
    """

    __DEFAULT_PREFIX__ = "/clingo"
    __DEFAULT_TAGS__ = ["Clingo"]

    def __init__(self, draco, **kwargs):
        c = ClingoRouter
        super().__init__(
            draco,
            prefix=kwargs.pop("prefix", c.__DEFAULT_PREFIX__),
            tags=kwargs.pop("tags", c.__DEFAULT_TAGS__),
            **kwargs,
        )

    @staticmethod
    def _register(router: "BaseDracoRouter"):
        @router.post("/run")
        def run(dto: endpoint_models.RunClingoDTO) -> endpoint_models.RunClingoReturn:
            return service.run_clingo(
                dto.program, dto.models, dto.topK, dto.arguments
            )  # pragma: no cover
