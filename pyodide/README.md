<!-- This file will be displayed as the main page of https://www.npmjs.com/package/draco-pyodide -->

# Draco Pyodide JavaScript Package

[![npm](https://img.shields.io/npm/v/draco-pyodide)](https://www.npmjs.com/package/draco-pyodide)
[![Pyodide Console](https://img.shields.io/badge/🐍%20launch-Pyodide%20Console-yellowgreen)](https://dig.cmu.edu/draco2/jupyterlite/static/pyodide/console.html)
[![PyPi](https://img.shields.io/pypi/v/draco.svg)](https://pypi.org/project/draco/)

## Usage

Apart from the Pyodide artifacts' location, the usage of `draco-pyodide` is identical to that of
[`pyodide`](https://www.npmjs.com/package/pyodide).

You can find tagged releases of the Draco Pyodide artifacts on our
[GitHub releases](https://github.com/cmudig/draco2/releases) page and commit-specific builds as GitHub Action artifacts
attached to [build workflows](https://github.com/cmudig/draco2/actions/workflows/build.yml).

### Node.js

Download the Draco Pyodide artifacts from [GitHub releases](https://github.com/cmudig/draco2/releases)
(`pyodide-*.tar.gz`) and extract its contents into a local directory (`./draco-pyodide-artifacts` in the example below)
The version of the release needs to match exactly the version of this package.

You can automate this using the following commands:

```shell
DRACO_PYODIDE_VERSION=2.0.0b4  # Replace with the package version of your choice
ARTIFACT_DIR=draco-pyodide-artifacts  # Replace with the directory of your choice
TAR_NAME=pyodide-$DRACO_PYODIDE_VERSION.tar.gz
wget https://github.com/cmudig/draco2/releases/download/v$DRACO_PYODIDE_VERSION/$TAR_NAME
mkdir $ARTIFACT_DIR
tar -xzf $TAR_NAME --directory $ARTIFACT_DIR
rm $TAR_NAME
```

Then you can load Draco Pyodide in Node.js as follows:

```javascript
// hello_draco.js
const { loadPyodide } = require("draco-pyodide");

async function hello_draco() {
  let pyodide = await loadPyodide({
    /* Draco Pyodide artifacts folder */
    indexURL: "./draco-pyodide-artifacts",
  });

  // Load our package
  await pyodide.loadPackage("draco");

  // Import the loaded `draco` package and access some attributes
  return pyodide.runPython(`
        import draco
        from draco.asp_utils import parse_blocks
        d = draco.Draco()
        
        # The final line of the code block is returned as the result
        f"Running draco version: {draco.__version__}", parse_blocks(d.hard), parse_blocks(d.soft)
      `);
}

hello_draco().then((result) => {
  // Destructure the returned list of Python objects
  const [version, hard, soft] = result;

  // Extract the constraint names from the Python `dict` objects
  const hardConstraintNames = Array.from(hard.keys()).slice(1);
  const softConstraintNames = Array.from(soft.keys()).slice(1);

  console.log(version);
  console.log(`=== Hard constraints ===\n${hardConstraintNames.join("\n")}`);
  console.log(`=== Soft constraints ===\n${softConstraintNames.join("\n")}`);
});
```

### Client-side JavaScript

When using Draco Pyodide in the browser, you can load the `draco-pyodide` package from `jsdelivr`. You can decide
whether you want to host the Draco Pyodide artifacts downloaded from
[GitHub releases](https://github.com/cmudig/draco2/releases) (`pyodide-*.tar.gz`) yourself or use the version hosted on
our GitHub Pages (`indexURL: "https://dig.cmu.edu/draco2/jupyterlite/static/pyodide"`).

⚠️Please note that most of the time you will want to host the artifacts yourself, since the ones hosted on our GitHub
Pages might be out of sync with the version of this package, caused by the fact that we redeploy the GitHub Pages site
each time we merge to `main`, but we only release a new version of this package when we do an actual tagged release.

```html
<!doctype html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/draco-pyodide@latest/pyodide.js"></script>
  </head>
  <body
    style="
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #1a1c40;
    "
  >
    <script type="text/javascript">
      async function main() {
        let pyodide = await loadPyodide({
          /* Draco Pyodide artifacts folder */
          indexURL: "https://dig.cmu.edu/draco2/jupyterlite/static/pyodide",
        });

        // Load our package
        await pyodide.loadPackage("draco");

        // Import the loaded `draco` package and access some attributes
        const [version, hard, soft] = await pyodide.runPython(`
          import draco
          d = draco.Draco()
          
          # The final line of the code block is returned as the result
          f"Running draco version: {draco.__version__}", d.hard, d.soft
        `);

        // Print the result of `f"Running draco version: {draco.__version__}"`
        console.log(version);
        console.log(`Hard constraints:\n${hard}`);
        console.log(`Soft constraints:\n${soft}`);
      }
      main();
    </script>
    <h1 style="color: #ffffff">Check the console for outputs</h1>
  </body>
</html>
```

### Further Examples

You can find a variety of examples in the [draco-web-examples](https://github.com/peter-gy/draco-web-examples)
repository, featuring more advanced usages of Draco in web applications.

## Details

The JavaScript code in this package is responsible for the following tasks:

1. Defines the public [JavaScript API](https://pyodide.org/en/stable/usage/api/js-api.html)
   - Package loading code to allow loading of other Python packages.
   - Can load [micropip](https://pyodide.org/en/stable/usage/api/micropip-api.html) to bootstrap loading of pure Python
     wheels
2. Loads the CPython interpreter and the core/pyodide emscripten application which embeds the interpreter.
3. Injects the `js/pyodide` JavaScript API into `sys.modules`. This is the final runtime dependency for `core/pyodide` &
   `py/pyodide`, so after this step the interpreter is fully up and running.
