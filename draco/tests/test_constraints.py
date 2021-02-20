from draco import is_satisfiable
from draco.programs import constraints, definitions

BASE_PROGRAMS = [definitions.program, constraints.program]


def test_domain_valid():
    assert is_satisfiable(BASE_PROGRAMS + ["attribute(mark_type,0,bar)."])


def test_domain_invlid():
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute(mark_type,0,invalid)."])


def test_duplicate_attribute():
    assert is_satisfiable(
        BASE_PROGRAMS + ["attribute(mark_type,0,bar).", "attribute(mark_type,1,line)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS + ["attribute(mark_type,0,bar).", "attribute(mark_type,0,line)."]
    )
