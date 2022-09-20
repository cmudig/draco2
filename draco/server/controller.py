from fastapi import FastAPI

import draco.server.models as models
import draco.server.service as service
import draco.server.utils as utils

app = FastAPI()


@app.post("/properties")
def get_properties(
    payload: models.PropertyDTO = models.PropertyDTO(),
    draco: models.DracoInitDTO = models.DracoInitDTO(),
) -> models.GetPropertiesReturn:
    return service.get_properties(
        names=payload.names, draco=service.draco_from_payload(draco)
    )


@app.post("/check-spec")
def check_spec(
    payload: models.CheckSpecDTO, draco: models.DracoInitDTO = models.DracoInitDTO()
) -> models.CheckSpecReturn:
    return service.check_spec(
        spec=payload.spec, draco=service.draco_from_payload(draco)
    )


@app.post("/complete-spec")
def complete_spec(
    payload: models.CompleteSpecDTO, draco: models.DracoInitDTO = models.DracoInitDTO()
) -> models.CompleteSpecReturn:
    generator = service.complete_spec(
        spec=payload.spec,
        num_models=payload.models,
        draco=service.draco_from_payload(draco),
    )
    return list(map(utils.model_to_jsonable_model, generator))


@app.post("/count-preferences")
def count_preferences(
    payload: models.CountPreferencesDTO,
    draco: models.DracoInitDTO = models.DracoInitDTO(),
) -> models.CountPreferencesReturn:
    return service.count_preferences(
        spec=payload.spec, draco=service.draco_from_payload(draco)
    )


@app.post("/get-violations")
def get_violations(
    payload: models.GetViolationsDTO, draco: models.DracoInitDTO = models.DracoInitDTO()
) -> models.GetViolationsReturn:
    return service.get_violations(
        spec=payload.spec, draco=service.draco_from_payload(draco)
    )


@app.post("/run-clingo")
def run_clingo(payload: models.RunClingoDTO) -> models.RunClingoReturn:
    generator = service.run_clingo(
        program=payload.program,
        num_models=payload.models,
        topK=payload.topK,
        arguments=payload.arguments,
    )
    return list(map(utils.model_to_jsonable_model, generator))
