from draco.programs import definitions


def test_has_definitions():
    assert len(definitions)


def test_definitions_has_marktype():
    assert "mark_type" in definitions
