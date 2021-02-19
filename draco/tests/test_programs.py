from draco.programs import constraints, definitions, generate, hard, helpers


def test_has_definitions():
    assert len(definitions.program)
    assert len(definitions.blocks)


def test_definitions_has_marktype():
    assert "mark_type" in definitions.blocks


def test_has_constraints():
    assert len(constraints.program)
    assert len(constraints.blocks)


def test_constraints_has_invalid_domain():
    assert "invalid_domain" in constraints.blocks


def test_has_generate():
    assert len(generate.program)
    assert len(generate.blocks)


def test_generate_has_marktype():
    assert "mark_type" in generate.blocks


def test_has_hard():
    assert len(hard.program)
    assert len(hard.blocks)


def test_has_helpers():
    assert len(helpers.program)
    assert len(helpers.blocks)
