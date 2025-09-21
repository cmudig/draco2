PACKAGE_ROOT = draco

all: lint typecheck cover book grounding-size

.PHONY: install
install:
	@echo "==> 📦 Installing Packages & Pre-Commit Hooks"
	@uv sync --all-extras --group dev --group docs --group typecheck --group lint --group test --frozen
	@uv run pre-commit install

.PHONY: test
test:
	@echo "==> 🧪 Tests"
	@uv run --all-extras pytest -svv $(PACKAGE_ROOT)

# Default coverage report format
COV_REPORT ?= term-missing

.PHONY: cover
cover:
	@echo "==> 🧪 Tests with Coverage =="
	@uv run --all-extras pytest --cov=./ --cov-report=$(COV_REPORT) $(PACKAGE_ROOT)

.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@uv run ruff format $(PACKAGE_ROOT) docs
	@uv run ruff check .

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@make mypy

.PHONY: mypy
mypy:
	@uv run --all-extras mypy --check-untyped-defs $(PACKAGE_ROOT)

.PHONY: jupyterlite-nb-patch
jupyterlite-nb-patch:
	@uv run --with nbformat python docs/jupyterlite_nb_patch.py

book:
	@echo "==> 📕 Book"
	@uv run --all-extras jupyter-book build docs
	@make jupyterlite-nb-patch

# This command does NOT support hot-reloading,
# but it is useful to quickly get a preview of how the deployed docs would look like.
# Especially useful for previewing `{eval-rst}` blocks.
.PHONY: book-serve
book-serve: book
	@echo "==> 📡 Serving Book at http://localhost:5000"
	@uv run python -m http.server --directory docs/_build/html --bind 0.0.0.0 5000

.PHONY: book-strict
book-strict:
	@uv run --all-extras jupyter-book build -W -n --keep-going docs
	@make jupyterlite-nb-patch

.PHONY: lab
lab:
	@uv run --all-extras jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.allow_origin="*"

.PHONY: build
build:
	@echo "==> 👷‍♀️ Build"
	@uv build -vvv

.PHONY: grounding-size
grounding-size: $(PACKAGE_ROOT)/asp/examples/*
	@echo "==> ⏚ Size of grounded program"
	@for file in $^ ; do \
		echo $${file} ; \
		uv run python -m clingo $(PACKAGE_ROOT)/asp/generate.lp $(PACKAGE_ROOT)/asp/constraints.lp $(PACKAGE_ROOT)/asp/define.lp $(PACKAGE_ROOT)/asp/helpers.lp $(PACKAGE_ROOT)/asp/hard.lp $${file} --text | wc -l ; \
	done

.PHONY: publish
publish: build
	@echo "==> 📰 Publish"
	@poetry publish --dry-run

.PHONY: clean
clean:
	@rm -rf .coverage
	@rm -rf dist
	@uv run jupyter-book clean docs
	@rm -f docs/.jupyterlite.doit.db
	@rm -rf docs/.cache
	@find . -type d -name '*.ipynb_checkpoints' -exec rm -r {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '.ruff_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
	@find . -type f -name ".coverage.*" -exec rm -rf {} +

.PHONY: serve
serve:
	@echo "==> 📡 Serve"
	@uv run --all-extras uvicorn draco.server.__main__:app --reload --host=0.0.0.0
