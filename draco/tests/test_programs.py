from draco.programs import constraints, definitions


def test_has_definitions():
    assert len(definitions)


def test_definitions_has_marktype():
    assert "mark_type" in definitions


def test_has_constraints():
    assert len(constraints)


def test_constraints_has_invalid_domain():
    assert "invalid_domain" in constraints
