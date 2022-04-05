from draco.asp_utils import Block
from draco.programs import define, helpers, soft
from draco.run import run_clingo


def list_preferences(program: str):
    try:
        model = next(run_clingo(helpers.program + define.program + program, 1))

        return [
            tuple(map(lambda x: x.name, symbol.arguments))
            for symbol in model.answer_set
            if symbol.name == "preference"
        ]
    except StopIteration:
        return None


def test_list_preferences():
    assert list_preferences(":- a. :- not a.") is None


def test_aggregate():
    b = soft.blocks["aggregate"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == [("aggregate", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    attribute((encoding,aggregate),e2,mean).
    """
        )
        == [("aggregate", "e1"), ("aggregate", "e2")]
    )


def test_bin():
    b = soft.blocks["bin"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,10).
    """
        )
        == [("bin", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,10).
    attribute((encoding,binning),e2,20).
    """
        )
        == [("bin", "e1"), ("bin", "e2")]
    )


def test_bin_high():
    b = soft.blocks["bin_high"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
     attribute((encoding,binning),e1,8).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,13).
    """
        )
        == [("bin_high", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,14).
    attribute((encoding,binning),e2,20).
    """
        )
        == [("bin_high", "e1"), ("bin_high", "e2")]
    )


def test_bin_low():
    b = soft.blocks["bin_low"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,8).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,3).
    """
        )
        == [("bin_low", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,binning),e1,7).
    attribute((encoding,binning),e2,3).
    """
        )
        == [("bin_low", "e1"), ("bin_low", "e2")]
    )


def test_encoding():
    b = soft.blocks["encoding"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    """
        )
        == [("encoding", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    """
        )
        == [("encoding", "e1"), ("encoding", "e2")]
    )


def test_encoding_field():
    b = soft.blocks["encoding_field"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,field),e1,temperature).
    """
        )
        == [("encoding_field", "e1")]
    )

    assert (
        list_preferences(
            b.program
            + """
    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
    """
        )
        == [("encoding_field", "e1"), ("encoding_field", "e2")]
    )


def test_same_field():
    b = soft.blocks["same_field"]
    assert isinstance(b, Block)

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,root,m).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,date).
    """
        )
        == []
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(encoding,m,e1).
    entity(encoding,m,e2).

    entity(mark,root,m).

    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    """
        )
        == [("same_field", "temperature")]
    )

    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,root,m).

    entity(encoding,m,e1).
    entity(encoding,m,e2).
    entity(encoding,m,e3).
    entity(encoding,m,e4).


    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,date).
    attribute((encoding,field),e4,date).
    """
        )
        == [("same_field", "temperature"), ("same_field", "date")]
    )

    # use field temperature twice with mark m1, and field date with 2 different marks
    assert (
        list_preferences(
            b.program
            + """
    entity(field,root,temperature).
    entity(field,root,date).

    entity(mark,root,m1).
    entity(mark,root,m2).

    entity(encoding,m1,e1).
    entity(encoding,m1,e2).
    entity(encoding,m2,e3).
    entity(encoding,m1,e4).


    attribute((encoding,field),e1,temperature).
    attribute((encoding,field),e2,temperature).
    attribute((encoding,field),e3,date).
    attribute((encoding,field),e4,date).
    """
        )
        == [("same_field", "temperature")]
    )
