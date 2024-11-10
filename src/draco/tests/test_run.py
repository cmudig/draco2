from unittest import TestCase

from draco import run_clingo


def test_run_all_models():
    models = list(run_clingo("{a;b;c}."))
    assert len(models) == 2**3


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


def test_model_string():
    m = next(run_clingo(["a.", "b."]))
    assert str(m) == "a.\nb."


def test_run_clingo_top_k():
    models = list(
        run_clingo(
            "2 { a(1..5) }. :- not a(2). #minimize { 1,X : a(X) }.",
            models=10,
            topK=True,
        )
    )
    assert len(models) == 10
    assert models[0].cost == [2]
    assert models[9].cost == [3]


def test_run_clingo_top_k_too_many():
    models = list(
        run_clingo(
            "{ a(1) }. :~ a(1). [1]",
            models=3,
            topK=True,
        )
    )
    assert len(models) == 2
    assert models[0].cost == [0]
    assert models[1].cost == [1]


def test_run_clingo_top_k_counts():
    for i in range(1, 20):
        models = list(
            run_clingo(
                "{ a(1..5) }. #minimize { 1,X : a(X) }.",
                models=i,
                topK=True,
            )
        )
        assert len(models) == i


def test_run_clingo_arguments():
    for c in [1, 2, 5]:
        model = next(
            run_clingo(
                " #const foo = 0. a(1..foo).",
                models=1,
                topK=False,
                arguments=[f"-c foo={c}"],
            )
        )
        count = 0
        for symbol in model.answer_set:
            if symbol.name == "a":
                count += 1

        assert count == c


def test_run_clingo_top_k_weight_rules():
    models = list(
        run_clingo(
            "{a(1..5)}. :- not a(3). :~ a(1..5). [1]",
            models=17,
            topK=True,
        )
    )
    assert len(models) == 16


class LoggingTest(TestCase):
    def test_run_clingo_top_k_all(self):
        with self.assertLogs() as cm:
            models = list(
                run_clingo(
                    "{ a(1..5) }. #minimize { 1,X : a(X) }.",
                    topK=True,
                )
            )
            self.assertEqual(len(cm.records), 1)
            self.assertEqual(
                cm.records[0].getMessage(),
                "Since all models should be computed, topK is ignored.",
            )
            assert len(models) == 2**5
