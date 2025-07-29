from dataclasses import dataclass
from typing import Any, Generator, Generic, Mapping, cast

import narwhals as nw
from narwhals.typing import IntoDataFrame, IntoDataFrameT

import draco as drc
from draco.renderer import AltairRenderer
from draco.renderer.altair.types import SpecificationDict as DracoChartModel
from draco.types import Specification


def _compute_weights_df(draco: drc.Draco) -> nw.DataFrame:
    return nw.from_dict(
        {
            "feature": [feature.replace("_weight", "") for feature in draco.weights],
            "weight": draco.weights.values(),
        },
        backend="pandas",
    )


@dataclass(frozen=True)
class DracoSessionState(Generic[IntoDataFrameT]):  # pytype: disable=invalid-annotation
    dracox: "DracoExpress"
    data: IntoDataFrameT
    spec: str
    weights: dict[str, int]


class DracoExpress:
    def __init__(
        self,
        draco: drc.Draco = drc.Draco(),
        program: str | drc.programs.Program = drc.programs.express,
    ):
        self.draco = draco
        self.program = (
            program.program if isinstance(program, drc.programs.Program) else program
        )
        self._weights_df = _compute_weights_df(draco)

    def dump_state(self, spec: str | list[str], data: IntoDataFrameT) -> IntoDataFrameT:
        nw_df = nw.from_native(data)
        backend = nw_df.implementation.name.lower()

        # Visualized data is part of the state
        data_df = nw.new_series(
            name="data",
            values=[nw_df.to_arrow().to_pylist()],
            backend=backend,
        ).to_frame()

        # Used programs are part of the state
        programs_df = nw.new_series(
            name="programs",
            values=[
                [
                    {"name": "define", "src": self.draco.define},
                    {"name": "constraints", "src": self.draco.constraints},
                    {"name": "helpers", "src": self.draco.helpers},
                    {"name": "generate", "src": self.draco.generate},
                    {"name": "hard", "src": self.draco.hard},
                    {"name": "soft", "src": self.draco.soft},
                    {"name": "optimize", "src": self.draco.optimize},
                    {"name": "express", "src": self.program},
                    {
                        "name": "spec",
                        "src": "\n".join(spec) if isinstance(spec, list) else spec,
                    },
                ]
            ],
            backend=backend,
        ).to_frame()

        # Current weights are part of the state
        weights_df = nw.new_series(
            name="weights",
            values=[self.weights_df.to_arrow().to_pylist()],
            backend=backend,
        ).to_frame()

        # Concatenate all parts of the state into a single dataframe
        return nw.concat(
            [data_df, programs_df, weights_df],
            how="horizontal",
        ).to_native()

    @classmethod
    def load_state(  # pytype: disable=not-indexable
        cls, state: IntoDataFrameT
    ) -> "DracoSessionState[IntoDataFrameT]":
        state_df = nw.from_native(state)

        # Recover dataframe by exploding and unnesting list of structs
        nested_data_df = state_df.select("data").explode("data")

        # Get the first row to extract the struct field names
        first_row = nested_data_df.head(1).to_arrow().to_pylist()[0]
        data_fields = (
            list(first_row["data"].keys()) if first_row and first_row["data"] else []
        )
        data_df = nested_data_df.select(
            *(nw.col("data").struct.field(field).alias(field) for field in data_fields)
        )

        # Recover programs so that we can reconstruct the Draco object
        programs: dict[str, str] = (
            state_df.select("programs")
            .explode("programs")
            .select(
                index=nw.lit(1),
                name=nw.col("programs").struct.field("name"),
                src=nw.col("programs").struct.field("src"),
            )
            .pivot("name", index="index")
            .drop("index")
            .to_arrow()
            .to_pylist()[0]
        )

        # Also recover weights so that we can assign them to the Draco object
        weights: dict[str, int] = (
            state_df.select("weights")
            .explode("weights")
            .select(
                index=nw.lit(1),
                feature=nw.col("weights").struct.field("feature"),
                weight=nw.col("weights").struct.field("weight"),
            )
            .with_columns(nw.concat_str([nw.col("feature"), nw.lit("_weight")]))
            .pivot("feature", index="index")
            .drop("index")
            .to_arrow()
            .to_pylist()[0]
        )

        draco = drc.Draco(
            define=programs["define"],
            constraints=programs["constraints"],
            helpers=programs["helpers"],
            generate=programs["generate"],
            hard=programs["hard"],
            soft=programs["soft"],
            optimize=programs["optimize"],
            weights=weights,
        )

        return DracoSessionState(
            dracox=cls(draco, programs["express"]),
            data=data_df.to_native(),
            spec=programs["spec"],
            weights=weights,
        )

    def with_weights(self, weights: dict[str, int]) -> "DracoExpress":
        weights_normalized = {
            (feature if feature.endswith("_weight") else f"{feature}_weight"): weight
            for feature, weight in weights.items()
        }
        draco_with_adjusted_weights = drc.Draco(
            define=self.draco.define,
            constraints=self.draco.constraints,
            helpers=self.draco.helpers,
            generate=self.draco.generate,
            hard=self.draco.hard,
            soft=self.draco.soft,
            optimize=self.draco.optimize,
            weights=self.draco.weights | weights_normalized,
        )
        return DracoExpress(draco_with_adjusted_weights)

    def with_draco(self, draco: drc.Draco) -> "DracoExpress":
        return DracoExpress(draco, self.program)

    @property
    def weights_df(self) -> nw.DataFrame:
        return self._weights_df

    def spec(self, spec: dict[str, Any]) -> "DracoChartSpec":
        return DracoChartSpec(self, spec)

    def complete_spec(
        self,
        spec: Specification,
        models: int = 1,
    ) -> Generator["DracoChartSpec", None, None]:
        fact_list = cast(list[str], spec if isinstance(spec, list) else [spec])
        spec_with_express_api = [self.program, *fact_list]
        for completion in self.draco.complete_spec(spec_with_express_api, models):
            yield DracoChartSpec(
                self,
                dict(drc.answer_set_to_dict(completion.answer_set)),
            )


def _compute_data_schema_facts(spec: dict[str, Any]) -> list[str]:
    relevant_keys = {"number_rows", "field"}
    return drc.dict_to_facts({k: v for k, v in spec.items() if k in relevant_keys})


def _compute_features_df(
    preferences: Mapping[str, int], weights_df: nw.DataFrame
) -> nw.DataFrame:
    return (
        nw.from_dict(
            {
                "feature": preferences.keys(),
                "count": preferences.values(),
            },
            backend="pandas",
        )
        .join(weights_df, on="feature", how="left")
        .select(
            "feature",
            cost=nw.col("weight") * nw.col("count"),
        )
        .sort("cost", descending=True)
    )


def _compute_observations_df(express_program: str, facts: list[str]) -> nw.DataFrame:
    program = [
        express_program,
        *facts,
        "#show observed/2.",
    ]
    result = list(drc.run_clingo(program))
    schema = nw.Schema({"subject": nw.String(), "value": nw.String()})
    if len(result) == 0:
        return nw.from_dict(
            {"subject": [], "value": []},
            backend="pandas",
            schema=schema,
        )
    observations = result[0].answer_set

    item_dict: dict[str, list[str]] = {
        "subject": [],
        "value": [],
    }
    for observation in observations:
        subject, value = observation.arguments
        item_dict["subject"].append(
            ", ".join([arg.name for arg in (subject.arguments or [subject])])
        )
        item_dict["value"].append(value.name)
    return nw.from_dict(item_dict, backend="pandas", schema=schema).sort("subject")


def _compute_chart_cost(features_df: nw.DataFrame) -> int:
    return int(features_df.select(nw.sum("cost")).to_numpy().squeeze())


class DracoChartSpec:
    def __init__(self, dracox: DracoExpress, spec: dict[str, Any]):
        self.dracox = dracox
        self.spec = spec
        self._data_schema_facts = _compute_data_schema_facts(spec)
        self._facts = drc.dict_to_facts(spec)
        self._features_df = _compute_features_df(
            self.draco.count_preferences(self._facts) or {},
            self.dracox.weights_df,
        )
        self._observations_df = _compute_observations_df(
            self.dracox.program,
            self._facts,
        )
        self._chart_cost = _compute_chart_cost(self._features_df)
        self._model = DracoChartModel.model_validate(spec)

    def __repr__(self) -> str:
        return repr(self.spec)

    @property
    def draco(self) -> drc.Draco:
        return self.dracox.draco

    @property
    def features_df(self) -> nw.DataFrame:
        return self._features_df

    @property
    def observations_df(self) -> nw.DataFrame:
        return self._observations_df

    @property
    def cost(self) -> int:
        return self._chart_cost

    @property
    def model(self) -> DracoChartModel:
        return self._model

    def render(self, df: IntoDataFrame):
        return AltairRenderer().render(self.spec, df)
