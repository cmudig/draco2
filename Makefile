all: lint mypy pytype pyright cover book check

test:
	@poetry run pytest -svv .

cover:
	@poetry run pytest --cov=draco --cov-report=term-missing .

lint:
	@poetry run black .
	@poetry run flake8 draco --statistics

mypy:
	@poetry run mypy -p draco

pytype:
	@poetry run pytype draco

pyright:
	@poetry run npx pyright

book:
	@poetry run jupyter-book build docs

book-strict:
	@poetry run jupyter-book build -W -n --keep-going docs

lab:
	@poetry run jupyter lab

build:
	@poetry build -vvv

check:
	@poetry check

publish: build
	@poetry publish --dry-run

clean:
	@jupyter-book clean docs
	@rm -rf .coverage
	@rm -rf dist
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
	@find . -type d -name '*.ipynb_checkpoints' -exec rm -r {} +
