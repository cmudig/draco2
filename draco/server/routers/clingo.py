import draco.server.models.clingo as endpoint_models
import draco.server.services.clingo as service

from .base import BaseDracoRouter


class ClingoRouter(BaseDracoRouter):
    """Router exposing clingo functionality through REST endpoints."""

    def __init__(self, draco, *args, **kwargs):
        super().__init__(draco, *args, **kwargs)

    @staticmethod
    def _register(router: "BaseDracoRouter"):
        @router.post("/run")
        def run(dto: endpoint_models.RunClingoDTO) -> endpoint_models.RunClingoReturn:
            return service.run_clingo(dto.program, dto.models, dto.topK, dto.arguments)
