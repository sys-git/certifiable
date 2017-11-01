FLAKE8_FORMAT ?= '$${cyan}%(path)s$${reset}:$${yellow_bold}%(row)d$${reset}:$${green_bold}%(col)d$${reset}: $${red_bold}%(code)s$${reset} %(text)s'
PYLINT_FORMAT ?= colorized

# This needs to go before we fiddle with paths.
SYSTEM_PYTHON := $(shell which python2.7)

#ifdef VIRTUAL_ENV
#$(error This Makefile cannot be run from inside a virtualenv)
#endif

VIRTUAL_ENV := $(abspath .virtualenv)
export VIRTUAL_ENV

PATH := $(abspath .virtualenv/bin):$(PATH)
export PATH

PYTHONPATH := $(abspath app):$(PYTHONPATH)
export PYTHONPATH

PIP := $(VIRTUAL_ENV)/bin/pip
TESTS ?= tests
NOSETESTS := $(VIRTUAL_ENV)/bin/nosetests
TOX := $(VIRTUAL_ENV)/bin/tox
FLAKE8 := $(VIRTUAL_ENV)/bin/flake8
PYLINT := $(VIRTUAL_ENV)/bin/pylint
VULTURE := $(VIRTUAL_ENV)/bin/vulture
RADON := $(VIRTUAL_ENV)/bin/radon
SPHINX_APIDOC := $(VIRTUAL_ENV)/bin/sphinx-apidoc
TESTS_ABS := $(foreach path,$(TESTS),$(abspath $(path)))

# The virtualenv is supposed to mirror what will already be present on
# app-engine. It also contains test dependencies.
.virtualenv:
	# Building python virtual environment
	$(SYSTEM_PYTHON) -m virtualenv -p $(SYSTEM_PYTHON) .virtualenv
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements/requirements.txt
	$(PIP) install --upgrade -r requirements/requirements-dev.txt
	$(PIP) install --upgrade -r requirements/requirements-test.txt
	# Update the last modified date on .virtualenv so that, if nothing has
	# changed, make knows not to rebuild it next time it runs.
	touch .virtualenv

.PHONY: build
build: .virtualenv


.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-docs: ## remove doc artifacts
	rm -fr docs/_build

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	$(FLAKE8) certifiable tests setup.py
	$(PYLINT) certifiable setup.py

test: ## run tests quickly with the default Python

	$(NOSETESTS) $(TESTS_ABS) -v --logging-level=INFO \
		--processes=-1 --process-timeout=240


tox: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python

	$(NOSETESTS) $(TESTS_ABS) -v --logging-level=INFO \
		--with-coverage --cover-erase \
		--cover-package=certifiable \
		--cover-html --cover-branches


	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/certifiable/certifiable.rst
	rm -f docs/certifiable/modules.rst
	$(SPHINX_APIDOC) -e -o docs/certifiable certifiable setup.py certifiable/complex.py certifiable/cli.py certifiable/core.py certifiable/operators.py certifiable/errors.py certifiable/utils.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
