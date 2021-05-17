.PHONY: install install-dev test

install:
	pip install -r requirements.txt

install-dev: install
	pre-commit install

lint:
	pre-commit run --all-files

test:
	coverage run -m pytest

coverage: test
	coverage report -m
	coverage html
