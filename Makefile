.PHONY: _prep create_environment requirements format lint docs docs-serve test \
	test-fastest test-debug-fastest _clean_manual_test manual-test manual-test-debug

## GLOBALS

PROJECT_NAME = cookiecutter-data-science
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python


###     UTILITIES
_prep:
	rm -f **/*/.DS_store


###     DEV COMMANDS

## Set up python interpreter environment
create_environment:
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -r dev-requirements.txt

## Format the code using isort and black
format:
	isort --profile black ccds hooks tests "{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}"
	black ccds hooks tests "{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}"
	
lint:
	flake8 ccds hooks tests "{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}"
	isort --check --profile black ccds hooks tests "{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}"
	black --check ccds hooks tests "{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}"


###     DOCS

docs:
	cd docs && mkdocs build

docs-serve:
	cd docs && mkdocs serve

###     TESTS

test: _prep
	pytest -vvv --durations=0

test-fastest: _prep
	pytest -vvv -FFF

test-debug-last:
	pytest --lf --pdb

_clean_manual_test:
	rm -rf manual_test

manual-test: _prep _clean_manual_test
	mkdir -p manual_test
	cd manual_test && python -m ccds ..

manual-test-debug: _prep _clean_manual_test
	mkdir -p manual_test
	cd manual_test && python -m pdb ../ccds/__main__.py ..
