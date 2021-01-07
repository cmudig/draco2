all: lint mypy cover book

develop:
	conda env create -f environment.yml
	conda activate draco
	python setup.py develop

test:
	pytest -s .

cover:
	pytest --cov=draco --cov-report=term-missing .

lint:
	black .
	flake8 draco --statistics

mypy:
	mypy -p draco

env-create:
	conda env create -f environment.yml
	conda activate draco

env-update:
	conda env update -f environment.yml

book:
	jupyter-book build docs

book-strict:
	jupyter-book build -W -n --keep-going docs

lab:
	jupyter lab

clean:
	jupyter-book clean docs
	rm .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	find '.' -name '*.ipynb_checkpoints' -exec rm -r {} +
	find '.' -name '__pycache__' -exec rm -r {} +
