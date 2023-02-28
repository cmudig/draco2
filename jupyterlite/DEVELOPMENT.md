# Draco & JupyterLite

We make Draco available through JupyterLite, a lightweight, browser-native Jupyter notebook. To do so, we have created a
custom distribution of [Pyodide](https://pyodide.org/en/stable/), enabling the bundling of Draco and all its
dependencies into WebAssembly modules which can be run directly in any modern browser. All the related heavy-lifting
takes place in the [pyodide](../pyodide) directory. You can read more about the technical details in the associated
[DEVELOPMENT.md](../pyodide/DEVELOPMENT.md). In this piece of documentation, we will take the existence of a custom
Pyodide distribution for granted and focus on how we wired it up with JupyterLite.

## Overview

The files in this directory are partial sources based on which we can build a complete JupyterLite bundle. The final
output will be a self-contained directory of HTML, CSS, JavaScript and WebAssembly files which can be served by any web
server. The directory structure of the output is as follows:

```text
.
├── DEVELOPMENT.md            # This file
├── build.py                  # Script to build the JupyterLite bundle
├── jupyter_lite_config.json  # High-level JupyterLite configuration file. Sets the output directory of the HTML bundle
└── lite-dir
    ├── files                 # JupyterLite-compatible `.ipynb` files
    ├── jupyter-lite.json     # Low-level JupyterLite configuration file, specifying plugins & site metadata
    └── static                # Place for static assets. Our custom Pyodide distro will be copied here by `build.py`
```

## Using the Custom Pyodide Distribution

We take advantage of the
[directory structure conventions](https://jupyterlite.readthedocs.io/en/latest/reference/cli.html#well-known-files) of
JupyterLite and place the custom Pyodide distribution in the `lite-dir/static/pyodide` directory. When building the
JupyterLite bundle, this is going to be copied into the final output directory automatically. We point to the custom
Pyodide entrypoint in `lite-dir/jupyter-lite.json#litePluginSettings`. This way, the Pyolite Kernel will use our custom
distribution instead of the default one. This is a crucial step: without this, we would not have access to Draco and all
the project dependencies, hence we would not be able to interact with Draco at all. That would be a shame, wouldn't it?

## Building the JupyterLite Bundle

The full HTML bundle can be built using the top-level `make jupyterlite-build` command. The following steps are taken:

1. The script looks for a local Pyodide distribution under `pyodide/pyodide-src/dist`. This is the location where
   `make pyodide-build` outputs the custom distro. If you did not build the distro from scratch using
   `make pyodide-build` beforehand, the script will download and use a pre-built distro.
2. The Pyodide distribution is copied into `lite-dir/static/pyodide`.
3. We run `jupyter lite build` from the `jupyterlite` directory. The output is place in the `/dist/jupyterlite`
   directory. This is specified in `jupyter_lite_config.json#LiteBuildConfig.output_dir`.

Since the output is self-contained, it is ready to be served. You can use any web server to do so. We provide
`make jupyterlite-serve` for convenience which starts a local web server on port 9999. You can then access the
JupyterLite app at [http://localhost:9999](http://localhost:9999).

Since we embed the Pyodide distribution into the JupyterLite bundle, we can also access the Pyodide console through the
JupyterLite app through
[http://localhost:9999/static/pyodide/console.html](http://localhost:9999/static/pyodide/console.html).

## Adding New Notebooks

The notebooks we have in the JupyterBook docs are **not** served by JupyterLite. Only the notebooks in `lite-dir/files`
are served by JupyterLite.

## Further Reading

- [JupyterLite Documentation](https://jupyterlite.readthedocs.io/en/latest/)
