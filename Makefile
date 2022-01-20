all: lint typecheck cover book check

.PHONY: test
test:
	@echo "==> 🧪 Tests"
	@poetry run pytest -svv .

.PHONY: cover
cover:
	@echo "==> 🧪 Tests with Coverage =="
	@poetry run pytest --cov=draco --cov-report=term-missing .

.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@poetry run black .
	@poetry run flake8 draco --statistics

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@make mypy pytype pyright

.PHONY: mypy
mypy:
	@poetry run mypy -p draco

.PHONY: pytype
pytype:
	@poetry run pytype draco

.PHONY: pyright
pyright:
	@npx pyright

book:
	@echo "==> 📕 Book"
	@poetry run jupyter-book build docs

.PHONY: book-strict
book-strict:
	@poetry run jupyter-book build -W -n --keep-going docs

.PHONY: lab
lab:
	@poetry run jupyter lab

.PHONY: build
build:
	@echo "==> 👷‍♀️ Build"
	@poetry build -vvv

.PHONY: check
check:
	@poetry check

.PHONY: publish
publish: build
	@echo "==> 📰 Publish"
	@poetry publish --dry-run

.PHONY: clean
clean:
	@jupyter-book clean docs
	@rm -rf .coverage
	@rm -rf dist
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
	@find . -type d -name '*.ipynb_checkpoints' -exec rm -r {} +
