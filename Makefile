all: lint mypy cover book check

test:
	@pytest -svv .

cover:
	@pytest --cov=draco --cov-report=term-missing .

lint:
	@black .
	@flake8 draco --statistics

mypy:
	@mypy -p draco

book:
	@jupyter-book build docs

book-strict:
	@jupyter-book build -W -n --keep-going docs

lab:
	@jupyter lab

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
