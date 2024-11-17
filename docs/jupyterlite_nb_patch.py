from os import PathLike
from pathlib import Path

import nbformat

DEFAULT_LITE_OUTPUT_DIR = str(Path(__file__).parent / "_build" / "html" / "lite")


# Each JupyterLite notebook's first cell will be set to this piece of code ensuring that the environment is set up correctly
PATCH_CELL_CODE = "%pip install draco"

# Actual notebook node with hidden source (collapsed by default in the UI)
PATCH_CELL = nbformat.v4.new_code_cell(
    PATCH_CELL_CODE,
    metadata={"tags": ["jupyterlite-only"], "jupyter": {"source_hidden": True}},
)


def patch_jupyterlite_notebooks(jupyterlite_output_dir: PathLike[str]):
    """
    Iterates over all ipynb files in the _build/lite/files directory and prepends the `PATCH_CELL` node to each notebook.

    We assume that the entire Sphinx build has been completed prior to running this function.
    :raises FileNotFoundError if the JupyterLite build directory is not found
    """
    jupyterlite_output_dir = Path(jupyterlite_output_dir)
    if not jupyterlite_output_dir.exists():
        raise FileNotFoundError(
            f"JupyterLite build directory not found at {jupyterlite_output_dir}."
        )

    notebook_paths = (jupyterlite_output_dir / "files").rglob("*.ipynb")
    for notebook_path in notebook_paths:
        print(f"Patching {notebook_path}")
        with open(notebook_path, "r") as f:
            nb = nbformat.read(f, as_version=4)
            nb.cells.insert(0, PATCH_CELL)
            with open(notebook_path, "w") as f:
                nbformat.write(nb, f)


if __name__ == "__main__":
    patch_jupyterlite_notebooks(DEFAULT_LITE_OUTPUT_DIR)
