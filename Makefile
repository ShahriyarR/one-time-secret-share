PYTHON=./.venv/bin/python

PHONY = help install install-dev test test-slow test-cov format lint type-check secure migrations migrate run

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To run application -> make run"
	@echo "To test the project type [exclude slow tests] -> make test"
	@echo "To test the project [only slow tests] -> make test-slow"
	@echo "To test with coverage [all tests] -> make test-cov"
	@echo "To format code type -> make format"
	@echo "To check linter type -> make lint"
	@echo "To run type checker -> make type-check"
	@echo "To run all security related commands -> make secure"
	@echo "To create database migrations -> make migrations"
	@echo "To run database migrations -> make migrate"
	@echo "------------------------------------"

install:
	${PYTHON} -m flit install --env --deps=production

install-dev:
	${PYTHON} -m flit install --env --deps=develop --symlink

test:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv -m "not slow and not integration" tests

test-integration:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv -m "integration" tests

test-slow:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv -m "slow" tests

test-django:
	${PYTHON} src/onetime/entrypoints/web/manage.py test onetime.entrypoints.web.onetimesecrets.tests

test-behave:
	${PYTHON} -m behave --show-timings --summary --capture --capture-stderr --logcapture --color

test-cov:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv --cov-report html --cov=src tests

format:
	${PYTHON} -m isort src tests --force-single-line-imports
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config pyproject.toml
	${PYTHON} -m isort src tests

lint:
	${PYTHON} -m flake8 src
	${PYTHON} -m black src tests --check --diff --config pyproject.toml
	${PYTHON} -m isort src tests --check --diff

type-check:
	${PYTHON} -m pytype --config=pytype.cfg src

secure:
	${PYTHON} -m bandit -r src --config pyproject.toml

run:
	cd src/onetime/entrypoints/web/; gunicorn --reload --workers=1 app.wsgi


run-dev:
	${PYTHON} src/onetime/entrypoints/web/manage.py runserver


collectstatic:
	${PYTHON} src/onetime/entrypoints/web/manage.py collectstatic
