from draco import is_satisfiable
from draco.programs import constraints, define

BASE_PROGRAMS = [define.program, constraints.program]


def test_domain_valid():
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((mark,type),0,bar)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((scale,type),0,linear)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((scale,channel),0,x)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((encoding,channel),0,x)."])
    assert is_satisfiable(
        BASE_PROGRAMS
        + [
            "entity(field,root,0).",
            "attribute((field,name),1,time).",
            "attribute((encoding,field),1,time).",
        ]
    )
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((encoding,aggregate),0,mean)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute((field,type),0,number)."])
    assert is_satisfiable(BASE_PROGRAMS + ["attribute(task,root,summary)."])


def test_domain_invalid():
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((mark,type),0,invalid)."])
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((scale,type),0,invalid)."])
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((scale,channel),0,invalid)."])
    assert not is_satisfiable(
        BASE_PROGRAMS + ["attribute((encoding,channel),0,invalid)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS
        + [
            "attribute((field,name),0,temperature).",
            "attribute((encoding,field),2,condition).",
        ]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS + ["attribute((encoding,aggregate),0,sum_mean)."]
    )
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((field,type),0,log)."])
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute(task,root,summary_task)."])


def test_duplicate_attribute():
    assert is_satisfiable(
        BASE_PROGRAMS
        + ["attribute((mark,type),0,bar).", "attribute((mark,type),1,line)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS
        + ["attribute((mark,type),0,bar).", "attribute((mark,type),0,line)."]
    )


def test_duplicate_field_name():
    assert is_satisfiable(
        BASE_PROGRAMS
        + [
            "attribute((field,name),0,temperature).",
            "attribute((field,name),1,time).",
        ]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS
        + [
            "attribute((field,name),0,temperature).",
            "attribute((field,name),1,temperature).",
        ]
    )


def test_fields():
    assert is_satisfiable(
        BASE_PROGRAMS
        + [
            "entity(field,root,0).",
            "attribute((field,name),0,foo).",
            "attribute((encoding,field),1,foo).",
        ]
    )
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((encoding,field),0,foo)."])


def test_facets():
    assert is_satisfiable(
        BASE_PROGRAMS
        + [
            "entity(field,root,0).",
            "attribute((field,name),0,foo).",
            "attribute((facet,field),1,foo).",
        ]
    )
    assert not is_satisfiable(BASE_PROGRAMS + ["attribute((facet,field),0,foo)."])


def test_attribute_entity():
    assert is_satisfiable(
        BASE_PROGRAMS + ["entity(mark,root,0).", "attribute((mark,type),0,bar)."]
    )
    assert not is_satisfiable(
        BASE_PROGRAMS + ["entity(invalid,root,0).", "attribute((mark,type),0,bar)."]
    )
