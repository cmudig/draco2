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


def test_bin_and_aggregate():
    b = hard.blocks["bin_and_aggregate"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).

    :- violation(_).
    """
    )

    # assert not is_satisfiable(
    #     p
    #     + """
    # entity(encoding,root,e1).
    # attribute((encoding,channel),e1,x).
    # attribute((encoding,binning),e1).
    # attribute((encoding,aggregate),e1,count).

    # :- violation(_).
    # """
    # )


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


def test_repeat_channel():
    b = hard.blocks["repeat_channel"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).


    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(scale,root,3).
    attribute((scale,channel),3,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    :- violation(_).
    """
    )


def test_row_no_y():
    b = hard.blocks["row_no_y"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    attribute((encoding,channel),e0,row).
    attribute((encoding,channel),e1,y).


    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,channel),e0,row).
    attribute((encoding,channel),e1,x).


    :- violation(_).
    """
    )


def test_encoding_no_field_and_not_count():
    b = hard.blocks["encoding_no_field_and_not_count"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).


    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).


    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).


    :- violation(_).
    """
    )


def test_count_with_field():
    b = hard.blocks["count_with_field"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).


    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).

    :- violation(_).
    """
    )


def test_point_tick_bar_without_x_or_y():
    b = hard.blocks["point_tick_bar_without_x_or_y"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,tick).
    attribute((encoding,channel),1,x).


    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,tick).

    :- violation(_).
    """
    )
