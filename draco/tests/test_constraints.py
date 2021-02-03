from draco import run_clingo
from draco.programs import constraints, definitions

BASE_PROGRAMS = [definitions.program, constraints.program]


def test_domain_valid():
    models = list(run_clingo(BASE_PROGRAMS + ["attribute(mark_type,v0,bar)."]))

    assert len(models) == 1


def test_domain_invlid():
    models = list(run_clingo(BASE_PROGRAMS + ["attribute(mark_type,v0,invalid)."]))

    assert len(models) == 0
