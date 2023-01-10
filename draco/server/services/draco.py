import draco.server.models.draco as endpoint_models
from draco import Draco
from draco.server.utils import model_to_jsonable_model
from draco.types import Specification


class DracoService:
    """
    Service exposing core functionality of :code:`Draco` through REST endpoints.
    Used by :code:`DracoRouter`.
    """

    def __init__(self, draco: Draco):
        """
        :param draco: :code:`Draco` instance to use.
        """
        self.draco = draco

    def check_spec(self, spec: Specification) -> endpoint_models.CheckSpecReturn:
        return self.draco.check_spec(spec)

    def complete_spec(
        self, spec: Specification, models: int
    ) -> endpoint_models.CompleteSpecReturn:
        generator = self.draco.complete_spec(spec, models)
        return list(map(model_to_jsonable_model, generator))

    def count_preferences(
        self, spec: Specification
    ) -> endpoint_models.CountPreferencesReturn:
        return self.draco.count_preferences(spec)

    def get_violations(
        self, spec: Specification
    ) -> endpoint_models.GetViolationsReturn:
        return self.draco.get_violations(spec)
