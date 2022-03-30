from draco.asp_utils import Block
from draco.programs import define, helpers, soft
from draco.run import is_satisfiable, run_clingo


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


def no_preferences(program: str):
    return is_satisfiable(
        helpers.program + define.program + program + ":- preference(_)."
    )


def test_list_preferences():
    assert list_preferences(":- a. :- not a.") is None


def test_aggregate():
    b = soft.blocks["aggregate"]
    assert isinstance(b, Block)

    assert no_preferences(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
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
