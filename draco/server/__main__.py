"""
Convenient entry-point for running the server
via :code:`python -m draco.server`.
"""

from fastapi import FastAPI

import draco.server.main as server_main
from draco.server import DracoAPI

# Extracting the `draco_api` and the `app` instances
# to allow calling `poetry run uvicorn draco.server.__main__:app --reload`
draco_api = DracoAPI()
app: FastAPI = draco_api.app

if __name__ == "__main__":
    nsp = server_main.DracoServerArgs()
    parser = server_main.argument_parser()
    parser.parse_known_args(namespace=nsp)
    server_main.main(draco_api=draco_api, args=nsp)
