from draco import run_clingo


def test_run_all_models():
    assert len(list(run_clingo("{a;b;c}."))) == 2 ** 3


def test_run_clingo_fact():
    run_clingo("fact(a,42).")


def test_run_clingo_no_opt():
    model = next(run_clingo("fact(a,42)."))

    assert model.cost == []
    assert model.number == 1


def test_run_clingo_opt():
    model = next(run_clingo("{a;b}. :~ a. [1]"))

    assert model.cost == [0]
    assert model.number == 1


def test_run_clingo_models():
    assert len(list(run_clingo("{a;b;c}.", models=2))) == 2


def test_run_clingo_list():
    next(run_clingo(["a.", "b."]))
