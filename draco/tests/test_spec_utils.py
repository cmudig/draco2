from draco import check_spec, get_violations
from draco.fact_utils import dict_to_facts


def test_check_spec():
    prog_valid = dict_to_facts(
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
    assert check_spec(prog_valid)

    prog_invalid = dict_to_facts(
        {
            "field": [{"name": "temperature", "type": "number"}],
            "mark": [
                {
                    # invalid mark
                    "type": "tickk",
                    "encoding": [{"channel": "x", "field": "temperature"}],
                }
            ],
            "scale": [{"channel": "x", "type": "linear"}],
        }
    )
    assert not check_spec(prog_invalid)


def test_get_violations():
    prog = dict_to_facts(
        {
            "field": [{"name": "temperature", "type": "number"}],
            "mark": [
                {
                    "type": "tickk",
                    "encoding": [{"channel": "x", "field": "temperature"}],
                }
            ],
            "scale": [{"channel": "x", "type": "linear"}],
        }
    )
    assert get_violations(prog) == ["invalid_domain"]


def test_get_violations_satisfiable():
    prog = ":- a."
    assert get_violations(prog) == ["no_encodings"]


def test_get_violations_unsatisfiable():
    prog = ":- a. :- not a."
    assert get_violations(prog) is None
