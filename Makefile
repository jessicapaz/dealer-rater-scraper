-include .env

install-dependencies:
	pip install pipenv
	pipenv install

lint:
	pipenv run flake8

test:
	pipenv run pytest tests
