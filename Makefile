all: lint typecheck cover book grounding-size check

.PHONY: test
test:
	@echo "==> 🧪 Tests"
	@poetry run pytest -svv draco

.PHONY: cover
cover:
	@echo "==> 🧪 Tests with Coverage =="
	@poetry run pytest --cov=draco --cov-report=term-missing .

.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@poetry run ruff format draco jupyterlite pyodide docs
	@poetry run ruff .

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@make mypy pytype pyright

.PHONY: mypy
mypy:
	@poetry run mypy -p draco --check-untyped-defs

.PHONY: pytype
pytype:
	@poetry run pytype draco

.PHONY: pyright
pyright:
	@poetry run npx --yes pyright@latest

book:
	@echo "==> 📕 Book"
	@poetry run jupyter-book build docs

# This command does NOT support hot-reloading,
# but it is useful to quickly get a preview of how the deployed docs would look like.
# Especially useful for previewing `{eval-rst}` blocks.
.PHONY: book-serve
book-serve: book
	@echo "==> 📡 Serving Book at http://localhost:5000"
	@poetry run python -m http.server --directory docs/_build/html --bind 0.0.0.0 5000

.PHONY: book-strict
book-strict:
	@poetry run jupyter-book build -W -n --keep-going docs

.PHONY: lab
lab:
	@poetry run jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.allow_origin="*"

.PHONY: build
build:
	@echo "==> 👷‍♀️ Build"
	@poetry build -vvv

.PHONY: check
check:
	@poetry check

.PHONY: grounding-size
grounding-size: ./draco/asp/examples/*
	@echo "==> ⏚ Size of grounded program"
	@for file in $^ ; do \
		echo $${file} ; \
		poetry run python -m clingo draco/asp/generate.lp draco/asp/constraints.lp draco/asp/define.lp draco/asp/helpers.lp draco/asp/hard.lp $${file} --text | wc -l ; \
	done

.PHONY: publish
publish: build
	@echo "==> 📰 Publish"
	@poetry publish --dry-run

.PHONY: clean
clean:
	@poetry run jupyter-book clean docs
	@rm -rf .coverage
	@rm -rf dist
	@rm -rf pyodide/pyodide-src
	@rm -rf jupyterlite/lite-dir/static/pyodide
	@rm -rf jupyterlite/lite-dir/files
	@rm -f jupyterlite/.jupyterlite.doit.db
	@find . -type d -name '.pytype' -exec rm -rf {} +
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
	@find . -type f -name ".coverage.*" -exec rm -rf {} +
	@find . -type d -name '*.ipynb_checkpoints' -exec rm -r {} +

.PHONY: serve
serve:
	@echo "==> 📡 Serve"
	@poetry run uvicorn draco.server.__main__:app --reload --host=0.0.0.0

.PHONY: pyodide-prepare
pyodide-prepare:
	@poetry run python pyodide/build.py --prepare

.PHONY: pyodide-finalize
pyodide-finalize:
	@poetry run python pyodide/build.py --finalize

.PHONY: pyodide-build
pyodide-build: pyodide-prepare
	@echo "==> 🐳 Building Pyodide Distribution"
	@cd pyodide/pyodide-src && ./run_docker --non-interactive bash -c './build_draco.sh'
	@make pyodide-finalize


.PHONY: jupyterlite-build
jupyterlite-build:
	@echo "==> 💡 Building Jupyter Lite Static Site"
	@cd jupyterlite && rm -rf lite-dir/static/pyodide && poetry run python build.py && poetry run jupyter lite build


# Re-using the Jupyter Lite build target, since it handles the download and 'caching' of our Pyodide distribution.
.PHONY: pyodide-serve
pyodide-serve: jupyterlite-build
	@echo "==> 📡 Serving Pyodide Console at http://localhost:9000/console.html"
	@poetry run python -m http.server --directory dist/jupyterlite/static/pyodide --bind 0.0.0.0 9000

.PHONY: jupyterlite-serve
jupyterlite-serve: jupyterlite-build
	@echo "==> 📡 Serving Jupyter Lite at http://localhost:9999"
	@poetry run python -m http.server --directory dist/jupyterlite --bind 0.0.0.0 9999
