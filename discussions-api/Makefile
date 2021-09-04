.ONESHELL:

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install:          ## Install the project in dev mode.
	poetry install
	poetry shell

.PHONY: run
run:			  ## Run the project in dev mode.
	python3 run.py

.PHONY: fmt
fmt:              ## Format code using black & isort.
	isort --recursive --force-single-line-imports --apply app
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
	black -l 79 app
	isort --recursive --apply

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	mypy app
	black -l 79 --check app
	isort --recursive --check-only app
	flake8 --max-line-length=79 app

.PHONY: test
test: lint		  ## Run tests and generate coverage report.
	pytest --cov=app --cov-report=term-missing --cov-report=html --tb=short --maxfail=1 tests

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .tox/
	rm -rf docs/_build
