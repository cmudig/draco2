from draco.programs import constraints, define, generate, hard, helpers


def test_has_define():
    assert len(define.program)
    assert len(define.blocks)


def test_define_has_marktype():
    assert "mark_type" in define.blocks


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
