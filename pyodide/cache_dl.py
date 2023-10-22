"""
Given a base URL to a hosted Pyodide distribution, we compare its `pyodide-lock.json`
with the local `pyodide/packages/*`.

If the remote lockfile includes a package of the same version
as the local recipe specifies, we download the remote artifacts
instead of building them locally from source.

If the local and remote Pyodide versions do not match, we build everything from source.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

import requests
import yaml


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


class LockfileInfo(TypedDict):
    arch: str
    platform: str
    version: str
    python: str


class LockfilePackage(TypedDict):
    name: str
    version: str
    file_name: str


class Lockfile(TypedDict):
    info: LockfileInfo
    packages: dict[str, LockfilePackage]


class RecipePackage(TypedDict):
    name: str
    version: str


class RecipeRequirements(TypedDict):
    host: list[str]
    run: list[str]


class Recipe(TypedDict):
    package: RecipePackage
    requirements: RecipeRequirements


def get_recipe_path(package_name: str) -> Path:
    return Path(__file__).parent / "packages" / package_name / "meta.yaml"


def load_recipe(package_name: str) -> Recipe | None:
    path = get_recipe_path(package_name)
    with open(path) as f:
        try:
            return yaml.safe_load(f)
        except FileNotFoundError:
            return None


def load_lockfile(lockfile_url: str) -> Lockfile | None:
    res = requests.get(lockfile_url)
    if res.status_code == 200:
        return json.loads(res.text)

    return None


def load_remote_artifact(url: str, name: str) -> bytes | None:
    url = f"{url}/{name}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.content

    return None


def load_dependent_packages_from_recipe(recipe: Recipe) -> set[str]:
    dependent_packages: set[str] = set()
    if "host" in recipe["requirements"]:
        dependent_packages.update(recipe["requirements"]["host"])
    if "run" in recipe["requirements"]:
        dependent_packages.update(recipe["requirements"]["run"])
    return dependent_packages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download prebuilt Pyodide artifacts")
    parser.add_argument(
        "--url",
        default="https://dig.cmu.edu/draco2/jupyterlite/static/pyodide",
        help="Base URL to a hosted Pyodide distribution",
    )
    parser.add_argument("--tag", default="0.24.1", help="Pyodide version tag")

    args = parser.parse_args()
    pyodide_url = args.url
    pyodide_tag = args.tag

    lockfile_url = f"{pyodide_url}/pyodide-lock.json"
    info(f"⬇️ Downloading lockfile from {lockfile_url}")
    lockfile = load_lockfile(lockfile_url)

    if lockfile is None:
        warn("🚧 Lockfile not found. Will build everything from source.")
        sys.exit(0)

    if lockfile["info"]["version"] != pyodide_tag:
        warn(
            "🚧 Pyodide version mismatch "
            f'(local: {pyodide_tag}, remote: {lockfile["info"]["version"]}). '
            "Will build everything from source."
        )
        sys.exit(0)

    # Dedicated set to track packages that need to be rebuilt
    # used to skip checking the same package multiple times
    # when encountering it as a dependency of other packages
    needs_rebuild: set[str] = set()

    for package in lockfile["packages"].values():
        package_name = package["name"].replace("-tests", "")
        recipe = load_recipe(package_name)
        if recipe is None:
            warn(f"🚧 Recipe not found for {package['name']}. Will build from source.")
            continue

        # Version specified in the lockfile we downloaded from the remote
        remote_version = str(package["version"]).lower().strip()
        # Version specified in the local pyodide git repository under /packages
        local_version = str(recipe["package"]["version"]).lower().strip()
        if remote_version != local_version:
            warn(
                f"🚧 {package['name']} version mismatch "
                f"(local: {local_version}, remote: {remote_version}). "
                "Will build from source."
            )
            needs_rebuild.add(package_name)
            continue

        info(f"⬇️ Downloading {package['file_name']}")
        content = load_remote_artifact(pyodide_url, package["file_name"])
        if content is None:
            warn(
                f"🚧 Failed to download {package['file_name']}. "
                "Will build from source."
            )
            needs_rebuild.add(package_name)
            continue

        # Write the downloaded prebuilt artifact to the local dist folder
        dist_folder = get_recipe_path(package_name).parent / "dist"
        dist_folder.mkdir(parents=True, exist_ok=True)
        info(f"📦 Saving {package['file_name']} to {dist_folder}")
        dist_folder.joinpath(package["file_name"]).write_bytes(content)

        # And mark it as built, as if we had built it from source
        build_folder = get_recipe_path(package_name).parent / "build"
        build_folder.mkdir(parents=True, exist_ok=True)
        info(f"👷 Marking package as built in {build_folder}")
        (build_folder / ".packaged").write_text("\n")

        package_has_no_dependencies = "requirements" not in recipe
        if package_has_no_dependencies:
            info(f"⏭️ {package['name']} has no dependencies")
            continue

        deps = load_dependent_packages_from_recipe(recipe)
        info(f"🔎 Dependencies of {package['name']}: {deps}")
        for dependent_pkg in deps:
            # We don't want to process a package that was already checked
            # or will be checked later
            pkg_will_be_checked_later = dependent_pkg in lockfile["packages"]
            if dependent_pkg in needs_rebuild:
                info(f"🚧 Dependent package {dependent_pkg} will be built from source")
                continue
            elif pkg_will_be_checked_later:
                info(f"⏭️ Dependent package {dependent_pkg} will be built later")
                continue

            # Reaching this point means that the dependent package
            # was **not** in the lockfile, therefore, it is a host dependency.
            # Host dependencies are needed to build a package, but we already
            # have the prebuilt package artifact, so we mark the host dep as built.
            build_folder = get_recipe_path(dependent_pkg).parent / "build"
            build_folder.mkdir(parents=True, exist_ok=True)
            packaged_token = build_folder / ".packaged"
            if not packaged_token.exists():
                info(
                    f"🖇️ Marking dependent package {dependent_pkg} "
                    f"as built in {build_folder}"
                )
                packaged_token.write_text("\n")
            else:
                info(
                    f"⏭️ Dependent package {dependent_pkg} "
                    f"already built in {build_folder}"
                )
