from draco import asp


def test_make_fact():
    assert asp.make_fact(("numberRows", 42)) == "fact(numberRows,42)."


def test_make_fact_short():
    assert asp.make_fact(("numberRows", 42), True) == "numberRows(42)."


def test_dict_to_facts():
    program = asp.dict_to_facts(
        {
            "numberRows": 42,
            "field": {
                "f1": {"unique": 12, "dataType": "number"},
                "f2": {"unique": 32, "dataType": "string"},
            },
        }
    )

    assert list(program) == [
        "fact(numberRows,42).",
        "fact(field,f1).",
        "fact(unique,f1,12).",
        "fact(dataType,f1,number).",
        "fact(field,f2).",
        "fact(unique,f2,32).",
        "fact(dataType,f2,string).",
    ]
