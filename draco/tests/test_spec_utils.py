from draco import check_spec
from draco.fact_utils import dict_to_facts


def test_tick_plot():
    prog = dict_to_facts(
        {
            "field": [{"name": "temperature", "type": "number"}],
            "mark": [
                {
                    "type": "tick",
                    "encoding": [{"channel": "x", "field": "temperature"}],
                }
            ],
            "scale": [{"channel": "x", "type": "linear"}],
        }
    )
    assert check_spec(prog)
