"""
Zero-dependency Python script to prepare a local environment
from which a JupyterLite site can be built using our custom Pyodide distro.

The script will attempt to use a local Pyodide distro build
if it exists under `pyodide/pyodide-src/dist`, otherwise
it will download a pre-built Pyodide distro from the latest release of cmudig/draco2.
"""
import json
import pathlib
import shutil
import sys
import tarfile
import urllib.request

LITE_DIR_PATH = pathlib.Path(__file__).parent / "lite-dir"
PYODIDE_DIST_LOCAL_PATH = (
    pathlib.Path(__file__).parent.parent / "pyodide" / "pyodide-src" / "dist"
)

# TODO: replace this with a cmudig/draco2 Pyodide release
PYODIDE_TARBALL_URL = (
    "https://github.com/peter-gy/draco-pyodide/releases/download/test/pyodide.tar.gz"
)
JUPYTER_LITE_CONFIG_JSON_PATH = (
    pathlib.Path(__file__).parent / "jupyter_lite_config.json"
)


def warn(msg: str) -> None:
    """
    Prints a warning message to stderr.

    :param msg: the warning message to print
    """
    WARN_COLOR = "\033[93m"
    ENDC = "\033[0m"
    print(f"{WARN_COLOR}Warning: {msg}{ENDC}", file=sys.stderr)


def info(msg: str) -> None:
    """
    Prints an info message to stdout.

    :param msg: the info message to print
    """
    INFO_COLOR = "\033[94m"
    ENDC = "\033[0m"
    print(f"{INFO_COLOR}Info: {msg}{ENDC}")


def read_jupyter_lite_config_json() -> dict:
    with open(JUPYTER_LITE_CONFIG_JSON_PATH, "r") as f:
        return json.load(f)


def extract_pyodide_tarball_to_static_dir(
    pyodide_tarball_url: str, lite_dir_path: pathlib.Path
):
    with urllib.request.urlopen(pyodide_tarball_url) as response:
        with tarfile.open(fileobj=response, mode="r|gz") as tar:
            tar.extractall(path=lite_dir_path)
            # rename ./build/pyodide/pyodide to ./build/static/pyodide
            (lite_dir_path / "pyodide").resolve().rename(
                lite_dir_path / "static" / "pyodide"
            )


def copy_local_dist_to_static_dir(
    pyodide_local_dist_path: pathlib.Path, lite_dir_path: pathlib.Path
):
    dest_path = lite_dir_path / "static" / "pyodide"
    shutil.copytree(pyodide_local_dist_path, dest_path)


def main():
    config = read_jupyter_lite_config_json()
    lite_dir_path = pathlib.Path(config["LiteBuildConfig"]["lite_dir"])
    static_path = lite_dir_path / "static"
    static_pyodide_path = static_path / "pyodide"

    if static_pyodide_path.exists():
        info("💪 Pyodide distro in static dir already exists, skipping extraction...")
    elif PYODIDE_DIST_LOCAL_PATH.exists():
        info("🏗Copying local Pyodide distro to static dir...")
        copy_local_dist_to_static_dir(PYODIDE_DIST_LOCAL_PATH, lite_dir_path)
    else:
        info(
            f"🧶Extracting pyodide tarball to static dir "
            f"from {PYODIDE_TARBALL_URL}..."
        )
        extract_pyodide_tarball_to_static_dir(PYODIDE_TARBALL_URL, lite_dir_path)


if __name__ == "__main__":
    main()
