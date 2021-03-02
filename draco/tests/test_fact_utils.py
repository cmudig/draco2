import itertools

import pytest
from draco.fact_utils import FactKind, dict_to_facts, facts_to_dict, make_fact
from draco.run import run_clingo


def test_make_attribute():
    assert (
        make_fact(FactKind.ATTRIBUTE, ("numberRows", "root", 42))
        == "attribute(numberRows,root,42)."
    )

    assert (
        make_fact(FactKind.ATTRIBUTE, ("XTest", "root", 42))
        == "attribute(xTest,root,42)."
    )

    assert (
        make_fact(FactKind.ATTRIBUTE, (("foo", "bar"), "root", 42))
        == "attribute((foo,bar),root,42)."
    )

    assert (
        make_fact(FactKind.ATTRIBUTE, (("foo"), "root", 42))
        == "attribute(foo,root,42)."
    )


def test_make_property():
    assert (
        make_fact(FactKind.PROPERTY, ("field", "root", "f1"))
        == "property(field,root,f1)."
    )


def test_dict_to_facts():
    program = dict_to_facts(
        {
            "numberRows": 42,
            "field": [
                {"unique": 12, "dataType": "number"},
                {"unique": 32, "dataType": "string"},
            ],
        }
    )

    assert list(program) == [
        # root
        "attribute(numberRows,root,42).",
        # first field
        "property(field,root,0).",
        "attribute(unique,0,12).",
        "attribute(dataType,0,number).",
        # second fields
        "property(field,root,1).",
        "attribute(unique,1,32).",
        "attribute(dataType,1,string).",
    ]


def test_dict_to_facts_start_id():
    program = dict_to_facts(
        {
            "field": [{"dataType": "number"}, {"dataType": "string"}],
        },
        id_generator=itertools.count(42),
    )

    assert list(program) == [
        # first field
        "property(field,root,42).",
        "attribute(dataType,42,number).",
        # second fields
        "property(field,root,43).",
        "attribute(dataType,43,string).",
    ]


def test_dict_to_facts_explicit_id():
    program = dict_to_facts(
        {
            "field": [{"dataType": "number", "__id__": "foo"}, {"dataType": "string"}],
        },
    )

    assert list(program) == [
        # first field
        "property(field,root,foo).",
        "attribute(dataType,foo,number).",
        # second fields
        "property(field,root,0).",
        "attribute(dataType,0,string).",
    ]


def test_deep_dict_to_facts():
    program = dict_to_facts(
        {
            "numberRows": 42,
            "field": [
                {
                    "dataType": "number",
                    "bin": [{"maxbins": 20}],
                },
            ],
        }
    )

    assert list(program) == [
        # root
        "attribute(numberRows,root,42).",
        # first field
        "property(field,root,0).",
        "attribute(dataType,0,number).",
        "property(bin,0,1).",
        "attribute(maxbins,1,20).",
    ]


def test_nested_dict_to_facts():
    program = dict_to_facts({"view": [{"scale": {"x": "linear"}}]})

    assert list(program) == [
        # root
        "property(view,root,0).",
        # first field
        "attribute((scale,x),0,linear).",
    ]


def test_nested_deep_dict_to_facts():
    program = dict_to_facts(
        {"view": [{"scale": {"x": {"type": "linear", "zero": "no"}}}]}
    )

    assert list(program) == [
        # root
        "property(view,root,0).",
        # first field
        "attribute((scale,x,type),0,linear).",
        "attribute((scale,x,zero),0,no).",
    ]


def test_false_dict_to_facts():
    program = dict_to_facts(
        {"view": [{"scale": {"x": {"type": "linear", "zero": False}}}]}
    )

    assert list(program) == [
        # root
        "property(view,root,0).",
        # first field
        "attribute((scale,x,type),0,linear).",
        ":- attribute((scale,x,zero),0).",  # note: this cannot be reversed
    ]


def test_true_dict_to_facts():
    program = dict_to_facts(
        {"view": [{"scale": {"x": {"type": "linear", "zero": True}}}]}
    )

    assert list(program) == [
        # root
        "property(view,root,0).",
        # first field
        "attribute((scale,x,type),0,linear).",
        "attribute((scale,x,zero),0).",  # note: this cannot be reversed
    ]


def test_dict_to_facts_string():
    """ We need at least some path. """
    program = dict_to_facts("foo")

    with pytest.raises(IndexError):
        list(program)


def test_dict_to_facts_complex():
    program = dict_to_facts(
        {
            "path1": {"path2": {"path3": [{"maxbins": 20}], "otherattr": 40}},
            "view": [
                {
                    "scale": {
                        "x": {
                            "type": "linear",
                            "metric": [
                                {"row_type": "number", "column_type": "number"},
                                {"row_num": 56, "column_num": 42},
                            ],
                            "zero": "false",
                        }
                    }
                },
                {"scale": "y"},
            ],
        }
    )

    assert list(program) == [
        "property((path1,path2,path3),root,0).",
        "attribute(maxbins,0,20).",
        "attribute((path1,path2,otherattr),root,40).",
        "property(view,root,1).",
        "attribute((scale,x,type),1,linear).",
        "property((scale,x,metric),1,2).",
        "attribute(row_type,2,number).",
        "attribute(column_type,2,number).",
        "property((scale,x,metric),1,3).",
        "attribute(row_num,3,56).",
        "attribute(column_num,3,42).",
        "attribute((scale,x,zero),1,false).",
        "property(view,root,4).",
        "attribute(scale,4,y).",
    ]


def test_facts_to_dict():
    program = [
        "attribute(numberRows,root,42).",
        "property(field,root,0).",
        "attribute(dataType,0,number).",
        "property(bin,0,1).",
        "attribute(maxbins,1,20).",
    ]

    for model in run_clingo(program):
        facts_to_dict(model.answer_set)
