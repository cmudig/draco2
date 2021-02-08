from draco.fact_utils import FactKind, dict_to_facts, facts_to_dict, make_fact


def test_make_attribute():
    assert (
        make_fact(FactKind.ATTRIBUTE, ("numberRows", "root", 42))
        == "attribute(numberRows,root,42)."
    )


def test_make_property():
    assert (
        make_fact(FactKind.PROPERTY, ("field", "root", "f1"))
        == "property(field,root,f1)."
    )


def test_make_fact_short():
    assert make_fact(FactKind.ATTRIBUTE, ("numberRows", 42), True) == "numberRows(42)."


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


def test_dict_to_facts_dict():
    program = dict_to_facts(
        {
            "numberRows": 42,
            "field": {
                "f1": {"unique": 12, "dataType": "number"},
                "f2": {"unique": 32, "dataType": "string"},
            },
        }
    )

    assert list(program) == [
        # root
        "attribute(numberRows,root,42).",
        # f1
        "property(field,root,f1).",
        "attribute(unique,f1,12).",
        "attribute(dataType,f1,number).",
        # f2
        "property(field,root,f2).",
        "attribute(unique,f2,32).",
        "attribute(dataType,f2,string).",
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


def test_facts_to_dict():
    # TODO
    facts_to_dict([])
