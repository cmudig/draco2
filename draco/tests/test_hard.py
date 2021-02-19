from draco import is_satisfiable
from draco.asp_utils import Block
from draco.programs import hard


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)

    assert is_satisfiable(
        b.program
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,text).

    :- violoation(_).
    """
    )

    assert is_satisfiable(
        b.program
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,text).

    :- violoation(_).
    """
    )

    assert not is_satisfiable(
        b.program
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,y).

    :- violoation(_).
    """
    )

    assert not is_satisfiable(
        b.program
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,y).
    attribute(channel,e3,text).

    :- violoation(_).
    """
    )
