from draco import run


def test_run_facts():
    run.run(facts=[("a"), ("b")])


def test_run_models():
    run.run(program="{a; b}.", models=2)
