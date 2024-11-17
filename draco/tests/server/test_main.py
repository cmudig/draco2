from multiprocessing import Process
from runpy import run_module

import pytest

import draco.server.main as server_main


@pytest.mark.parametrize(
    "raw_args,expected_ns",
    [
        ([], server_main.DracoServerArgs(**server_main.__DEFAULT_ARGS__.__dict__)),
        (
            ["--port", "1234"],
            server_main.DracoServerArgs(
                **(server_main.__DEFAULT_ARGS__.__dict__ | {"port": 1234})
            ),
        ),
        (
            ["--host", "some-host"],
            server_main.DracoServerArgs(
                **(server_main.__DEFAULT_ARGS__.__dict__ | {"host": "some-host"})
            ),
        ),
        (
            ["--reload"],
            server_main.DracoServerArgs(
                **(server_main.__DEFAULT_ARGS__.__dict__ | {"reload": True})
            ),
        ),
        (
            ["--reload", "--port", "1234", "--host", "some-host"],
            server_main.DracoServerArgs(
                **(
                    server_main.__DEFAULT_ARGS__.__dict__
                    | {"reload": True, "port": 1234, "host": "some-host"}
                )
            ),
        ),
        (
            ["--show-routes"],
            server_main.DracoServerArgs(
                **(server_main.__DEFAULT_ARGS__.__dict__ | {"show_routes": True})
            ),
        ),
    ],
)
def test_argument_parser(raw_args: list[str], expected_ns: server_main.DracoServerArgs):
    parser = server_main.argument_parser()
    ns = server_main.DracoServerArgs()
    parser.parse_args(raw_args, namespace=ns)
    assert ns == expected_ns


def test_show_routes(capsys: pytest.CaptureFixture):
    args = server_main.DracoServerArgs(show_routes=True)
    server_main.main(args=args)

    captured = capsys.readouterr()
    output = captured.out.strip()
    expected_headers = ["Name", "Path", "Methods", "Tags"]
    for header in expected_headers:
        assert header in output


def test_start_server_via_main():
    p = Process(target=server_main.main)
    p.start()
    # wait for the server to start
    p.join(2.5)
    assert p.is_alive()
    p.terminate()


def run_draco_server_module():
    # run the module as if it was called via `python -m draco.server`
    run_module("draco.server", run_name="__main__")


def test_start_server_via_cli():
    p = Process(target=run_draco_server_module)
    p.start()
    # wait for the server to start
    p.join(2.5)
    assert p.is_alive()
    p.terminate()
