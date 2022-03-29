from typing import Iterable, Union

from draco import dict_to_facts
from draco.asp_utils import Block
from draco.programs import define, helpers, soft
from draco.run import is_satisfiable, run_clingo
from draco.tests.test_hard import list_violations, no_violations


def test_aggregate():
    b = soft.blocks["aggregate"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    """
        )
        == ["aggregate"]
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((encoding,aggregate),e1,mean).
    attribute((encoding,aggregate),e2,mean).
    """
        )
        ==  ["aggregate"] * 2
    )

