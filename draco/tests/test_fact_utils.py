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
        start_id=42,
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


def test_facts_to_dict():
    program1 = [
        "attribute(numberRows,root,42).",
        "property(field,root,0).",
        "attribute(dataType,0,number).",
        "property(bin,0,1).",
        "property(bin,0,2).",
        "attribute(maxbins,2,20)." "attribute(maxbins,1,20).",
    ]

    program2 = dict_to_facts(
        {"view": [{"scale": {"x": {"type": "linear", "zero": False}}}]}
    )

    program3 = dict_to_facts(
        {
            "view": [
                {
                    "scale": {
                        "x": {"type": "linear", "metric": "numeric", "zero": False}
                    }
                },
                {"scalar": "numeric"},
            ]
        }
    )

    program4 = dict_to_facts(
        {
            "path1": {"path2": {"path3": [{"maxbins": 20}], "otherattr": 40}},
            "view": [
                {
                    "scale": {
                        "x": {
                            "type": "linear",
                            "metric": [
                                {"rowtype": "number", "columntype": "number"},
                                {"rownum": 56, "columnNum": 42},
                            ],
                            "zero": False,
                        }
                    }
                },
                {"scale": "y"},
            ],
        }
    )
    for model in run_clingo(program1):
        facts_to_dict(model.answer_set)
    for model in run_clingo(program2):
        facts_to_dict(model.answer_set)
    for model in run_clingo(program3):
        facts_to_dict(model.answer_set)
    for model in run_clingo(program4):
        facts_to_dict(model.answer_set)
