from draco import is_satisfiable
from draco.programs import constraints, definitions

BASE_PROGRAMS = [definitions.program, constraints.program]


def test_domain_valid():
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((mark,type),0,bar)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((scale,type),0,linear)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((scale,channel),0,x)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((encoding,channel),0,x)."])


def test_domain_invlid():
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((mark,type),0,invalid)."])
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((scale,type),0,invalid)."])
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((scale,channel),0,invalid)."])
    assert not is_satisfiable(
        BASE_PROGRAMS + ["attribute((encoding,channel),0,invalid)."]
    )


def test_duplicate_attribute():
    assert is_satisfiable(
        BASE_PROGRAMS
        + ["attribute((mark,type),0,bar).", "attribute((mark,type),1,line)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS
        + ["attribute((mark,type),0,bar).", "attribute((mark,type),0,line)."]
    )


def test_fields():
    assert is_satisfiable(
        BASE_PROGRAMS
        + ["attribute((field,name),0,foo).", "attribute((encoding,field),1,foo)."]
    )
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((encoding,field),0,foo)."])


def test_attribute_property():
    assert is_satisfiable(
        BASE_PROGRAMS + ["property(mark,root,0).", "attribute((mark,type),0,bar)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS + ["property(invalid,root,0).", "attribute((mark,type),0,bar)."]
    )
