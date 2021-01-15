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
    assert make_fact(None, ("numberRows", 42), True) == "numberRows(42)."


def test_dict_to_facts():
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


def test_facts_to_dict():
    # TODO
    facts_to_dict([])
