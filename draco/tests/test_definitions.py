from draco.definitions import definitions


def test_has_definitions():
    assert len(definitions)


def test_has_marktype():
    assert "marktype" in definitions
