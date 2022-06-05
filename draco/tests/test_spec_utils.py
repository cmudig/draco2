from draco import check_spec, get_violations
from draco.fact_utils import dict_to_facts
from draco.spec import count_preferences


def test_check_spec():
    prog_valid = dict_to_facts(
        {
            "field": [
                {"name": "temperature", "type": "number", "__id__": "temperature"}
            ],
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
            "field": [
                {"name": "temperature", "type": "number", "__id__": "temperature"}
            ],
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
            "field": [
                {"name": "temperature", "type": "number", "__id__": "temperature"}
            ],
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
    assert get_violations(prog) == ["invalid_domain"]


def test_get_violations_satisfiable():
    assert get_violations("") == []


def test_get_violations_unsatisfiable():
    prog = ":- a. :- not a."
    assert get_violations(prog) is None


def test_count_preferences():
    prog = dict_to_facts(
        {
            "field": [
                {"name": "temperature", "type": "number", "__id__": "temperature"},
                {"name": "city", "type": "number", "__id__": "city"},
            ],
            "mark": [
                {
                    "type": "point",
                    "encoding": [
                        {"channel": "y", "field": "temperature"},
                        {"channel": "x", "field": "city"},
                    ],
                }
            ],
            "scale": [
                {"channel": "y", "type": "linear"},
                {"channel": "x", "type": "ordinal"},
            ],
        }
    )

    assert count_preferences(prog) == {
        "c_d_point": 1,
        "continuous_not_zero": 1,
        "continuous_pos_not_zero": 1,
        "encoding": 2,
        "encoding_field": 2,
        "linear_scale": 1,
        "linear_y": 1,
        "ordinal_scale": 1,
        "ordinal_x": 1,
    }


def test_count_preferences_satisfiable():
    assert count_preferences("") == {}


def test_count_preferences_unsatisfiable():
    prog = ":- a. :- not a."
    assert count_preferences(prog) is None
