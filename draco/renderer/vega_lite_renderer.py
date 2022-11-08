import json

from pandas import DataFrame

from .base_renderer import BaseRenderer, VisitedItem


class VegaLiteRenderer(BaseRenderer[dict]):
    def __init__(self, spec: dict, df: DataFrame):
        super().__init__(spec, df)

    @property
    def _initial(self) -> dict:
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.2.0.json",
        }

    def _visitor(self, item: VisitedItem) -> dict:
        match item.type:
            case "mark":
                pass
            case "encoding":
                pass
            case "scale":
                pass
        return item.acc

    def post_build_hook(self, product: dict) -> dict:
        # add data to VL spec
        data = self.df.to_dict(orient="records")
        product["data"] = {"values": data}
        return product

    __DATA_TYPE_MAP__ = {
        "number": "quantitative",
        "string": "nominal",
    }


if __name__ == "__main__":
    from pprint import pprint

    from draco.fact_utils import answer_set_to_dict
    from draco.run import run_clingo

    def facts_to_dict(facts: list[str]):
        result = run_clingo(facts)
        return answer_set_to_dict(next(result).answer_set)

    facts = [
        "attribute(number_rows,root,100).",
        "entity(field,root,temperature).",
        "attribute((field,name),temperature,temperature).",
        "attribute((field,type),temperature,number).",
        "entity(view,root,0).",
        "entity(mark,0,1).",
        "attribute((mark,type),1,tick).",
        "entity(encoding,1,2).",
        "attribute((encoding,channel),2,x).",
        "attribute((encoding,field),2,temperature).",
        "entity(scale,0,3).",
        "attribute((scale,channel),3,x).",
        "attribute((scale,type),3,linear).",
    ]
    spec = facts_to_dict(facts)

    pprint(spec)
    print()

    df = DataFrame.from_records(
        data=[dict(a=i, b=25 * i, c=50 * i) for i in range(1, 11)]
    )
    vl = VegaLiteRenderer(dict(spec), df)
    product = vl.build()
    print(json.dumps(product, indent=2))
