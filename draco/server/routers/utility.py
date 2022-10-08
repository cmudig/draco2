import draco.server.models.utility as endpoint_models
import draco.server.services.utility as service

from .base import BaseDracoRouter


class UtilityRouter(BaseDracoRouter):
    def __init__(self, draco, *args, **kwargs):
        super().__init__(draco, *args, **kwargs)

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
