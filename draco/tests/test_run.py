from draco import run_clingo


def test_run_all_models():
    models = list(run_clingo("{a;b;c}."))
    assert len(models) == 2 ** 3


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


def test_run_clingo_top_k():
    for i in range(1, 15):
        models = list(
            run_clingo(
                "2 { a(1..5) }. :- not a(2). #minimize { 1,X : a(X) }.",
                models=i,
                topK=True,
            )
        )
        assert len(models) == i
        assert models[0].cost == [2]
