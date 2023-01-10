import argparse

import uvicorn

from .draco_api import DracoAPI


class DracoServerArgs(argparse.Namespace):
    """Namespace for the CLI arguments expected from the user."""

    host: str
    port: int
    reload: bool


__DEFAULT_ARGS__ = DracoServerArgs(host="127.0.0.1", port=8000, reload=False)


def argument_parser() -> argparse.ArgumentParser:
    """
    Create an argument parser for the Draco server CLI.

    :return: the argument parser used to collect arguments from the user.
    """
    parser = argparse.ArgumentParser(
        description="FastAPI Server exposing the capabilities of Draco",
        usage="python -m draco.server [options]",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=__DEFAULT_ARGS__.host,
        help=f"Host to run server on. Defaults to {__DEFAULT_ARGS__.host}",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=__DEFAULT_ARGS__.port,
        help=f"Port to run server on. Defaults to {__DEFAULT_ARGS__.port}",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=__DEFAULT_ARGS__.reload,
        help="Enable auto-reloading of the server on code changes.",
    )
    return parser


def main(
    draco_api: DracoAPI | None = None,
    args: DracoServerArgs = __DEFAULT_ARGS__,
):
    """
    Run the Draco server.

    :param draco_api: the DracoAPI object to use for the server.
    :param args: the arguments to use in the :code:`uvicorn.run` call.
    """
    uvicorn.run(
        (draco_api or DracoAPI()).app,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
