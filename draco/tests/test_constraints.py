from draco import run_clingo
from draco.asp_utils import blocks_to_program
from draco.programs import constraints, definitions

BASE_PROGRAMS = blocks_to_program(definitions) + blocks_to_program(constraints)


def test_domain_valid():
    models = list(run_clingo(BASE_PROGRAMS + ["attribute(mark_type,v0,bar)."]))

    assert len(models) == 1


def test_domain_invlid():
    models = list(run_clingo(BASE_PROGRAMS + ["attribute(mark_type,v0,invalid)."]))

    assert len(models) == 0
