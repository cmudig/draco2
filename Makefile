all: lint mypy test

test:
	pytest .

cover:
	pytest --cov=draco --cov-report=term-missing .

lint:
	black .
	flake8 . --statistics

mypy:
	mypy -p draco

env-create:
	conda env create -f environment.yml
	conda activate draco

env-update:
	conda env update -f environment.yml
