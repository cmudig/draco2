from draco import is_satisfiable
from draco.asp_utils import Block
from draco.programs import hard, helpers, generate, definitions


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).

    :- violation(_).
    """
    )


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

# def test_bin_and_aggregate():
#     b = hard.blocks["bin_and_aggregate"]
#     assert isinstance(b, Block)
#     p = b.program + definitions.program + generate.program

#     # assert is_satisfiable(
#     #     p
#     #     + """
#     # entity(encoding,root,e2).
#     # attribute((encoding,channel),e2,x).
#     # attribute((encoding,field),e2,temperature).
#     # attribute((encoding,binning),e2).
#     # entity(encoding,root,e3).
#     # attribute((encoding,channel),e3,y).
#     # attribute((encoding,aggregate),e3,count).

#     # :- violation(_).
#     # """
#     # )

#     assert is_satisfiable(
#         p
#         + """
#     entity(encoding,root,e2).
#     attribute(channel,e2,x).
#     attribute(field,e2,temperature).
#     attribute(binning,e2).
#     entity(encoding,root,e3).
#     attribute(channel,e3,y).
#     attribute(aggregate,e3,count).

#     :- violation(_).
#     """
#     )
#     # assert not is_satisfiable(
#     #     p
#     #     + """
#     # entity(encoding,root,e2).
#     # attribute((encoding,channel),e2,x).
#     # attribute((encoding,field),e2,temperature).
#     # attribute((encoding,binning),e2).
#     # attribute((encoding,aggregate),e2,count).

#     # :- violation(_).
#     # """
#     # )
#     assert not is_satisfiable(
#         p
#         + """
#     entity(encoding,root,e2).
#     attribute(channel,e2,x).
#     attribute((encoding,field),e2,temperature).
#     attribute(binning,e2).
#     attribute(aggregate,e2,count).

#     :- violation(_).
#     """
#     )
def test_no_encodings():
    b = hard.blocks["no_encodings"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    entity(encoding,root,e1).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,channel),e2,x).

    :- violation(_).
    """
    )