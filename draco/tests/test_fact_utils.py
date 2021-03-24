import itertools

import pytest
from draco.fact_utils import FactKind, answer_set_to_dict, dict_to_facts, make_fact
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
                {"unique": 12, "type": "number"},
                {"unique": 32, "type": "string"},
            ],
        }
    )

    assert list(program) == [
        # root
        "attribute(numberRows,root,42).",
        # first field
        "property(field,root,0).",
        "attribute((field,unique),0,12).",
        "attribute((field,type),0,number).",
        # second fields
        "property(field,root,1).",
        "attribute((field,unique),1,32).",
        "attribute((field,type),1,string).",
    ]


def test_dict_to_facts_start_id():
    program = dict_to_facts(
        {
            "field": [{"type": "number"}, {"type": "string"}],
        },
        id_generator=itertools.count(42),
    )

    assert list(program) == [
        # first field
        "property(field,root,42).",
        "attribute((field,type),42,number).",
        # second fields
        "property(field,root,43).",
        "attribute((field,type),43,string).",
    ]


def test_dict_to_facts_explicit_id():
    program = dict_to_facts(
        {
            "field": [{"type": "number", "__id__": "foo"}, {"type": "string"}],
        },
    )

    assert list(program) == [
        # first field
        "property(field,root,foo).",
        "attribute((field,type),foo,number).",
        # second fields
        "property(field,root,0).",
        "attribute((field,type),0,string).",
    ]


def test_deep_dict_to_facts():
    program = dict_to_facts(
        {
            "numberRows": 42,
            "field": [
                {
                    "type": "number",
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
        "attribute((field,type),0,number).",
        "property(bin,0,1).",
        "attribute((bin,maxbins),1,20).",
    ]


def test_false_dict_to_facts():
    program = dict_to_facts({"zero": False})

    assert list(program) == [
        ":- attribute(zero,root).",  # note: this cannot be reversed
    ]


def test_true_dict_to_facts():
    program = dict_to_facts({"zero": True})

    assert list(program) == [
        "attribute(zero,root).",  # note: this cannot be reversed
    ]


def test_dict_to_facts_string():
    """ We need at least some path. """
    program = dict_to_facts("foo")

    with pytest.raises(IndexError):
        list(program)


def test_dict_to_facts_complex():
    program = dict_to_facts(
        {
            "view": [
                {
                    "mark": [
                        {"type": "bar", "encoding": [{"channel": "x", "field": "foo"}]}
                    ],
                    "scale": [{"channel": "x", "type": "linear"}],
                }
            ],
        }
    )

    assert list(program) == [
        "property(view,root,0).",
        "property(mark,0,1).",
        "attribute((mark,type),1,bar).",
        "property(encoding,1,2).",
        "attribute((encoding,channel),2,x).",
        "attribute((encoding,field),2,foo).",
        "property(scale,0,3).",
        "attribute((scale,channel),3,x).",
        "attribute((scale,type),3,linear).",
    ]


def test_answer_set_to_dict():
    program = [
        # root
        "attribute(numberRows,root,42).",
        # first field
        "property(field,root,0).",
        "attribute((field, unique),0,12).",
        "attribute((field,type),0,number).",
        # second fields
        "property(field,root,1).",
        "attribute((field, unique),1,32).",
        "attribute((field,type),1,string).",
    ]

    result = run_clingo(program)
    assert answer_set_to_dict(next(result).answer_set) == {
        "numberRows": 42,
        "field": [
            {"unique": 12, "type": "number"},
            {"unique": 32, "type": "string"},
        ],
    }
