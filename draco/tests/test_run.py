from draco import run


def test_run_clingo_models():
    run.run_clingo(program="{a; b}.", models=2)


def test_run_clingo_list():
    run.run_clingo(program=["a.", "b."])
