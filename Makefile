-include .env

install-dependencies:
	python -m pip install --upgrade pip
	pip install pipenv
	pipenv install

lint:
	flake8 .

test:
	pytest tests
