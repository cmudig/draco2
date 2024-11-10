import argparse

import uvicorn

from . import utils
from .draco_api import DracoAPI


class DracoServerArgs(argparse.Namespace):
    """Namespace for the CLI arguments expected from the user."""

    host: str
    port: int
    reload: bool
    show_routes: bool


__DEFAULT_ARGS__ = DracoServerArgs(
    host="127.0.0.1", port=8000, reload=False, show_routes=False
)


def argument_parser() -> argparse.ArgumentParser:
    """
    Create an argument parser for the Draco server CLI.

    :return: the argument parser used to collect arguments from the user.
    """
    parser = argparse.ArgumentParser(
        description="FastAPI Server exposing the capabilities of Draco",
        usage="python -m draco.server [options]",
    )

    # Options related to running the server
    run_group = parser.add_argument_group(
        "Run Options", "Options related to running the server"
    )
    run_group.add_argument(
        "--host",
        type=str,
        default=__DEFAULT_ARGS__.host,
        help=f"Host to run server on. Defaults to {__DEFAULT_ARGS__.host}",
    )
    run_group.add_argument(
        "--port",
        type=int,
        default=__DEFAULT_ARGS__.port,
        help=f"Port to run server on. Defaults to {__DEFAULT_ARGS__.port}",
    )
    run_group.add_argument(
        "--reload",
        action="store_true",
        default=__DEFAULT_ARGS__.reload,
        help="Enable auto-reloading of the server on code changes.",
    )

    # Options related to the server utilities
    utility_group = parser.add_mutually_exclusive_group()
    utility_group.add_argument(
        "--show-routes",
        action="store_true",
        default=__DEFAULT_ARGS__.show_routes,
        help="Show the routes registered by the server and exit",
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
    used_draco_api = draco_api or DracoAPI()

    if args.show_routes:
        print(utils.tabulate_routes(used_draco_api.app))
        return

    uvicorn.run(
        used_draco_api.app,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
