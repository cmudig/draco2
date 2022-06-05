import pytest
from draco import Draco
from draco.fact_utils import dict_to_facts

default_draco = Draco()


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
    assert default_draco.check_spec(prog_valid)

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
    assert not default_draco.check_spec(prog_invalid)


def test_check_spec_custom_draco():
    d = Draco(hard="violation(no_point) :- attribute((mark,type),_,point),")

    prog_valid = dict_to_facts({"mark": [{"type": "point"}]})
    assert not default_draco.check_spec(prog_valid)
    assert d.check_spec(prog_valid)


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
    assert default_draco.get_violations(prog) == ["invalid_domain"]


def test_get_violations_satisfiable():
    assert default_draco.get_violations("") == []


def test_get_violations_unsatisfiable():
    prog = ":- a. :- not a."
    assert default_draco.get_violations(prog) is None


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

    assert default_draco.count_preferences(prog) == {
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
    assert default_draco.count_preferences("") == {}


def test_count_preferences_unsatisfiable():
    prog = ":- a. :- not a."
    assert default_draco.count_preferences(prog) is None


def test_weight_mismatch():
    with pytest.raises(AssertionError):
        Draco(weights={})
