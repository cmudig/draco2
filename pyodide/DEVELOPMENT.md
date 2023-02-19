# Draco Meets Pyodide

## Rationale

To ensure a seamless interaction with Draco, we aim to simplify its operation as a web-based application. Although Draco
already features an [intuitive server component](https://dig.cmu.edu/draco2/applications/server.html), some users may
prefer a trial run of the library. Additionally, when integrating Draco into a larger system, the maintenance of a
separate server may not be desired. To address these needs, we have created a custom distribution using
[Pyodide](https://pyodide.org/en/stable/), enabling the bundling of Draco and all its dependencies into WebAssembly
modules which can be run directly in any modern browser.

## Building Our Custom Pyodide Distribution

To construct our custom distribution, we heavily relied on the
[official Pyodide documentation](https://pyodide.org/en/stable/development/building-from-sources.html#using-docker) and
augmented the described steps to meet our specific needs.

### The `./packages` Directory

Pyodide uses "build recipes" to create WebAssembly modules from individual Python packages. The cornerstone of these
build recipes is a [meta.yaml specification](https://pyodide.org/en/stable/development/meta-yaml.html), which outlines
the Python source to be transformed into a WebAssembly module and its dependencies.

Although Pyodide already has a vast collection of build recipes in its
[repository](https://github.com/pyodide/pyodide/tree/main/packages), it lacks support for some of the dependencies
required to bundle Draco. To overcome this, we have created our own build recipes in the [./packages](./packages)
directory.

#### The `draco` Build Recipe

To make Draco accessible on the web, we must also create a build recipe for it. Unlike the other build recipes we
maintain, the version, wheel URL, and checksum of the package cannot be directly specified in the meta.yaml file, as we
are simultaneously developing both the Pyodide distribution and Draco, and therefore it must be built from source every
time. To account for these dynamic values, we created a [meta.yaml.template](./packages/draco/meta.yaml.template) for
Draco, in which we define the static values of the recipe and replace the template variables at build time.

#### The `pyodide-requirements.txt` File

As previously mentioned, Pyodide already has a substantial number of build recipes for Python packages. These can be
included in our custom distribution by listing them in the
[pyodide-requirements.txt](./packages/pyodide-requirements.txt) file. It's important to note that the file should have
one package name per line and that the names used should match those in the
[Pyodide repository](https://github.com/pyodide/pyodide/tree/main/packages).

### The `build.py` Script

The [build.py](./build.py) script is accountable for constructing our custom Pyodide distribution from the Draco git
tree. It performs the following steps:

1. Builds Draco from source
2. Creates the build recipe for Draco from the template, deriving the template variables' value from the build step's
   output
3. Clones a pre-specified tag of [Pyodide](https://github.com/pyodide/pyodide)
4. Copies the built Draco wheel into the Pyodide repository
5. Copies the build recipes from the [./packages](./packages) directory into the Pyodide repository
6. Registers the packages specified in the [pyodide-requirements.txt](./packages/pyodide-requirements.txt) file
7. Builds the Pyodide distribution inside a Docker container based on
   [pyodide/pyodide-env](https://hub.docker.com/r/pyodide/pyodide-env) provided by Pyodide

Running `make pyodide-build` from the root directory of the repository will complete all necessary steps. The custom
Pyodide distribution will be located in the pyodide/pyodide-src/dist folder when the build is finished.
