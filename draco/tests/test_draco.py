import pytest

from draco import Draco
from draco.fact_utils import answer_set_to_dict, dict_to_facts

default_draco = Draco()


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
    assert default_draco.check_spec(prog_valid)

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
    assert not default_draco.check_spec(prog_invalid)


def test_check_spec_custom_draco():
    d = Draco(hard="violation(no_point) :- attribute((mark,type),_,point),")

    prog_valid = dict_to_facts({"mark": [{"type": "point"}]})
    assert not default_draco.check_spec(prog_valid)
    assert d.check_spec(prog_valid)


def test_get_violations():
    prog = dict_to_facts(
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
        "c_d_overlap_point": 1,
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


def test_complete_histogram():
    partial_spec = """
    attribute(number_rows,root,100).

    entity(field,root,(f,0)).
    attribute((field,name),(f,0),temperature).
    attribute((field,type),(f,0),number).
    attribute((field,unique),(f,0),100).

    entity(view,root,(v,0)).

    entity(mark,(v,0),(m,0)).
    entity(encoding,(m,0),(e,0)).
    attribute((encoding,field),(e,0),temperature).
    attribute((encoding,binning),(e,0),10).
    """.split()

    assert default_draco.get_violations(partial_spec) == []
    model = next(default_draco.complete_spec(partial_spec))
    assert model.number == 1

    spec = answer_set_to_dict(model.answer_set)
    mark = spec["view"][0]["mark"][0]
    encodings = mark["encoding"]

    assert len(encodings) == 2
    assert mark["type"] == "bar"
