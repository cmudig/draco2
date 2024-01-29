"""
Zero-dependency Python script to build a custom Pyodide distribution,
relying on a basic Unix shell environment with `poetry` and `docker` installed.
"""
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys

# All paths are relative to the root of draco's git root
PYODIDE_BUILD_MODULE_ROOT_PATH = pathlib.Path(".") / "pyodide"
PYODIDE_PACKAGES_PATH = PYODIDE_BUILD_MODULE_ROOT_PATH / "packages"
PYODIDE_REQUIREMENTS_PATH = PYODIDE_PACKAGES_PATH / "pyodide-requirements.txt"
PYODIDE_REPO_NAME = "pyodide-src"
PYODIDE_REPO_PATH = PYODIDE_BUILD_MODULE_ROOT_PATH / PYODIDE_REPO_NAME
PYODIDE_REPO_URL = "https://github.com/pyodide/pyodide.git"
PYODIDE_REPO_TAG = "0.24.1"

# Directory where the Pyodide distribution will be built
PYODIDE_DIST_PATH = PYODIDE_REPO_PATH / "dist"

# Path to the Pyodide package.json file and to the template to be merged with it
PACKAGE_JSON_REAL_PATH = PYODIDE_DIST_PATH / "package.json"
PACKAGE_JSON_TEMPLATE_PATH = (
    PYODIDE_BUILD_MODULE_ROOT_PATH / "package-patch.json.template"
)

# Paths relative to the root of the docker container
DOCKER_PYODIDE_REPO_ROOT = pathlib.Path("/src")


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


def error(msg: str) -> None:
    """
    Prints an error message to stderr and exits with code 1.

    :param msg: the error message to print
    """
    ERROR_COLOR = "\033[91m"
    ENDC = "\033[0m"
    print(f"{ERROR_COLOR}Error: {msg}{ENDC}", file=sys.stderr)
    sys.exit(1)


def sh(cmd: str) -> str:
    """
    Simply utility function to run a shell command,
    handling command argument splitting by default.

    :param cmd: the shell command to run
    :return: the output of the command as a stripped string
    """
    return subprocess.check_output(shlex.split(cmd)).decode().strip()


def find_git_repo_root() -> pathlib.Path:
    """
    Finds the root directory of the git repository
    that contains this file.

    :return: path to the root of the git repository
    """
    return pathlib.Path(__file__).parent.parent.resolve()


def build_draco() -> None:
    """
    Builds the Draco library.
    """
    sh("poetry build")


def get_draco_wheel_path(draco_repo_root: pathlib.Path) -> pathlib.Path:
    """
    Gets the path to the built Draco wheel.

    :return: the path to the built Draco wheel
    """
    dist_dir = draco_repo_root / "dist"
    return next(dist_dir.glob("draco-*.whl"))


def copy_draco_build_to_pyodide_repo(draco_repo_root: pathlib.Path) -> None:
    """
    Copies the built Draco wheel to the Pyodide repository.
    """
    wheel_path = get_draco_wheel_path(draco_repo_root)
    shutil.copy(wheel_path, PYODIDE_REPO_PATH / wheel_path.name)


def get_draco_build_version() -> str:
    """
    Gets the version of the Draco library that was built.

    :return: the version of the Draco library that was built
    """
    return sh("poetry version -s")


def get_sha256_sum(file_path: pathlib.Path) -> str:
    """
    Gets the SHA256 hash of the supplied `file_path`.

    :param file_path: the path to the file to hash
    :return: the SHA256 hash of the supplied `file_path`
    """
    return sh(f"sha256sum {file_path}").split(" ")[0]


def get_draco_wheel_data(
    draco_repo_root: pathlib.Path = find_git_repo_root(),
    docker_pyodide_repo_root: pathlib.Path = DOCKER_PYODIDE_REPO_ROOT,
) -> tuple:
    """
    Returns an url to the built wheel and its SHA256 hash as a tuple.

    :return: wheel URL and the wheel's SHA256 hash as a tuple
    """
    wheel_path = get_draco_wheel_path(draco_repo_root)
    wheel_name = wheel_path.name
    docker_full_wheel_path = docker_pyodide_repo_root / wheel_name
    wheel_url = f"file://{docker_full_wheel_path.resolve()}"
    sha256 = get_sha256_sum(wheel_path.resolve())
    return wheel_url, sha256


def get_draco_build_recipe_template_data() -> dict:
    """
    :return: a dictionary containing the data to use in
             `pyodide/packages/draco/meta.yaml.template`
    """
    package_version = get_draco_build_version()
    wheel_url, sha256 = get_draco_wheel_data(find_git_repo_root())
    return {
        "package_version": package_version,
        "source_url": wheel_url,
        "source_sha256": sha256,
    }


def render_template_string(template: str, data: dict) -> str:
    """
    Renders the supplied `template` string using the supplied `data`.
    `template` is expected to be a Python format string.

    :param template: the template string to render
    :param data: the data to use when rendering the template
    :return: the rendered template string
    """
    return template.format(**data)


def build_draco_custom_recipe() -> None:
    """
    Builds the custom Draco package recipe from
    `pyodide/packages/draco/meta.yaml.template`and
    writes it to `pyodide/packages/draco/meta.yaml`.
    """
    template_data = get_draco_build_recipe_template_data()
    template = (PYODIDE_PACKAGES_PATH / "draco" / "meta.yaml.template").read_text()
    rendered = render_template_string(template, template_data)
    (PYODIDE_PACKAGES_PATH / "draco" / "meta.yaml").write_text(rendered)


def list_custom_packages(packages_path: pathlib.Path = PYODIDE_PACKAGES_PATH) -> list:
    """
    Lists all the custom package recipes in the supplied `packages_path`.

    :param packages_path: the path to the directory containing the custom packages
    :return: a list of the names of the custom packages
    """
    dirs = [d for d in packages_path.iterdir() if d.is_dir()]
    return [d.name for d in dirs]


def copy_package_recipe_to_pyodide_repo(
    package_name: str,
    packages_path: pathlib.Path = PYODIDE_PACKAGES_PATH,
    pyodide_repo_path: pathlib.Path = PYODIDE_REPO_PATH,
) -> None:
    """
    Copies the package recipe for the supplied `package_name`
    from the supplied `packages_path`to the supplied `pyodide_repo_path`.

    :param package_name: the name of the package to copy
    :param packages_path: the path to the directory containing the custom packages
    :param pyodide_repo_path: the path to the Pyodide repository
    """
    package_path = packages_path / package_name
    if not package_path.exists():
        error(f"Package {package_name} does not exist in {packages_path}")

    pyodide_packages_path = pyodide_repo_path / "packages"
    pyodide_package_path = pyodide_packages_path / package_name
    if pyodide_package_path.exists():
        warn(f"{pyodide_package_path} exists. Overwriting it with custom recipe...")
        shutil.rmtree(pyodide_package_path)

    # Create dir & copy package
    shutil.copytree(package_path, pyodide_package_path)


def clone_pyodide_repo(
    git_url: str = PYODIDE_REPO_URL,
    pyodide_repo_path: pathlib.Path = PYODIDE_REPO_PATH,
    pyodide_repo_tag: str = PYODIDE_REPO_TAG,
) -> None:
    """
    Clones the Pyodide repository to the supplied `pyodide_repo_path`.

    :param git_url: the URL of the Pyodide repository
    :param pyodide_repo_path: the path to clone the Pyodide repository to
    :param pyodide_repo_tag: the tag of the Pyodide repository to clone
    """
    sh(f"git clone {git_url} {pyodide_repo_path} --branch {pyodide_repo_tag}")


def install_recipe_cmd(package_name: str) -> str:
    """
    Returns the command to install the package recipe for the supplied `package_name`.

    :param package_name: the name of the package to install
    :return: the command to install the package recipe
    """
    return f"pyodide build-recipes {package_name} --install"


def load_pyodide_requirements(
    pyodide_requirements_path: pathlib.Path = PYODIDE_REQUIREMENTS_PATH,
) -> list:
    """
    :return: a list of the packages listed in `pyodide/requirements.txt`
    """
    return [
        line
        for line in pyodide_requirements_path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


def copy_cache_dl_script_to_pyodide_src(
    pyodide_repo_path: pathlib.Path = PYODIDE_REPO_PATH,
) -> None:
    """
    Copies `cache_dl.py` to the Pyodide repository.

    :param pyodide_repo_path: the path to the Pyodide repository
    """
    file_path = PYODIDE_BUILD_MODULE_ROOT_PATH / "cache_dl.py"
    shutil.copy(file_path, pyodide_repo_path)


def create_distro_build_script(pyodide_requirements: list) -> None:
    packages_to_install = [*pyodide_requirements, "draco"]
    recipe_installation_cmds = [install_recipe_cmd(p) for p in packages_to_install]

    # We need additional components to build `pydantic-core` properly,
    # as it is written in Rust
    pydantic_core_buildenv = [
        "pip install maturin",
        "rustup install nightly",
        "rustup default nightly",
        "rustup target add wasm32-unknown-emscripten",
    ]

    # Executing our custom cache downloader script
    pyodide_cache_dl = [
        "pip install pyyaml",
        f"python cache_dl.py --tag {PYODIDE_REPO_TAG}",
    ]

    script_body = "\n".join(
        [
            "#!/bin/bash",
            "python -m pip install --upgrade pip",
            "pip install -e pyodide-build",
            *pyodide_cache_dl,
            *pydantic_core_buildenv,
            "make",
            *recipe_installation_cmds,
        ]
    )
    script_path = (PYODIDE_REPO_PATH / "build_draco.sh").resolve()
    script_path.write_text(script_body)
    script_path.chmod(0o755)


def package_json_template_data() -> dict:
    return {"version": get_draco_build_version()}


def update_package_json():
    package_json_tmpl_content = json.loads(PACKAGE_JSON_TEMPLATE_PATH.read_text())
    package_json_tmpl_data: dict = package_json_template_data()
    package_json_updated_content = {
        **package_json_tmpl_content,
        **package_json_tmpl_data,
    }
    package_json_content_real: dict = json.loads(PACKAGE_JSON_REAL_PATH.read_text())
    merged = {**package_json_content_real, **package_json_updated_content}
    PACKAGE_JSON_REAL_PATH.write_text(json.dumps(merged, indent=2))


def prepare():
    git_repo_root = find_git_repo_root().resolve()
    current_dir = os.getcwd()
    # Normalize current working directory
    if current_dir != str(git_repo_root):
        warn(
            "You are not in the root of the git repository. "
            f"Changing cwd to {git_repo_root}..."
        )
        os.chdir(git_repo_root)

    info(f"🚧Executing actions from {os.getcwd()}")

    info("🏗️Building Draco...")
    build_draco()

    info("🧑‍🍳Building custom Draco package recipe...")
    build_draco_custom_recipe()

    custom_packages = list_custom_packages()
    info(f"📦Found custom packages: {custom_packages}")

    if PYODIDE_REPO_PATH.exists():
        warn(f"{PYODIDE_REPO_PATH} already exists. Deleting it...")
        sh(f"rm -rf {PYODIDE_REPO_PATH}")

    info(f"🐙Cloning Pyodide repository to {PYODIDE_REPO_PATH}...")
    clone_pyodide_repo()

    info("🛞Copying built Draco wheel to Pyodide repository...")
    copy_draco_build_to_pyodide_repo(git_repo_root)

    for package in custom_packages:
        info(f"📦Copying {package} recipe to Pyodide repository...")
        copy_package_recipe_to_pyodide_repo(package)

    info("📄Loading Pyodide requirements...")
    pyodide_requirements = load_pyodide_requirements()
    for package in pyodide_requirements:
        info(f"📦Found Pyodide requirement: {package}")

    info("📄Copying cache downloader script to Pyodide repository...")
    copy_cache_dl_script_to_pyodide_src()

    info("📄Creating distro build script...")
    create_distro_build_script(pyodide_requirements)


def finalize():
    git_repo_root = find_git_repo_root().resolve()
    current_dir = os.getcwd()
    # Normalize current working directory
    if current_dir != str(git_repo_root):
        warn(
            "You are not in the root of the git repository. "
            f"Changing cwd to {git_repo_root}..."
        )
        os.chdir(git_repo_root)

    info(f"🚧Executing actions from {os.getcwd()}")
    info("📄Updating package.json...")
    update_package_json()


if __name__ == "__main__":
    # check for --prepare flag
    if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
        prepare()
    elif len(sys.argv) > 1 and sys.argv[1] == "--finalize":
        finalize()
    else:
        error("Please specify either --prepare or --finalize")
