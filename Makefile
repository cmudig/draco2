all: lint mypy cover book check

develop:
	@conda env create -f environment.yml
	@conda activate draco
	@python setup.py develop

test:
	@pytest -svv .

cover:
	@pytest --cov=draco --cov-report=term-missing .

lint:
	@black .
	@flake8 draco --statistics

mypy:
	@mypy -p draco

env-create:
	@conda env create -f environment.yml
	@conda activate draco

env-update:
	@conda env update -f environment.yml

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
