import draco.server.models.utility as endpoint_models
import draco.server.services.utility as service

from .base import BaseDracoRouter


class UtilityRouter(BaseDracoRouter):
    """Router exposing utility functionality through REST endpoints."""

    __DEFAULT_PREFIX__ = "/utility"
    __DEFAULT_TAGS__ = ["Utility"]

    def __init__(self, draco, **kwargs):
        c = UtilityRouter
        super().__init__(
            draco,
            prefix=kwargs.pop("prefix", c.__DEFAULT_PREFIX__),
            tags=kwargs.pop("tags", c.__DEFAULT_TAGS__),
            **kwargs,
        )

    @staticmethod
    def _register(router: "BaseDracoRouter") -> None:
        @router.post("/dict-to-facts")
        def dict_to_facts(
            dto: endpoint_models.DictToFactsDTO,
        ) -> endpoint_models.DictToFactsReturn:
            return service.dict_to_facts(dto.data)  # pragma: no cover

        @router.post("/answer-set-to-dict")
        def answer_set_to_dict(
            dto: endpoint_models.AnswerSetToDictDTO,
        ) -> endpoint_models.AnswerSetToDictReturn:
            return service.answer_set_to_dict(dto.answer_set)  # pragma: no cover
