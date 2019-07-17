PYTEST_OPTIONS = -v

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help              to show this message"
	@echo "  all               to to execute lint and test-coverage."
	@echo "  install           to install conduit-qe if only running tests"
	@echo "  install-dev       to install conduit-qe in editable mode to"
	@echo "                    develop test cases"
	@echo "  lint              to lint the source code"
	@echo "  test              to run conduit-qe's framework unit tests"
	@echo "  test-coverage     to run conduit-qe's unit tests and measure"
	@echo "                    test coverage"
	@echo "  test-api          to run functional tests against rhsm-conduit"
	@echo "                    api endpoints"
	@echo "  clean             to remove all saved logs and cached python files"
	@echo "  uninstall         to uninstall conduit-qe's virtual environment"

all: lint test-coverage

install:
	pipenv install

install-dev:
	pipenv install --dev

lint:
	pipenv run flake8 conduitqe tests

test:
	pipenv run pytest $(PYTEST_OPTIONS) tests

test-api:
	pipenv run pytest $(PYTEST_OPTIONS) conduitqe/tests/api/


test-coverage:
	pipenv run pytest $(PYTEST_OPTIONS) --verbose \
		--cov-report term --cov=conduitqe --cov=tests tests

clean:
	rm -rf conduitqe.egg-info/
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

uninstall:
	pipenv --rm || true

.PHONY: all install install-dev lint test test-coverage test-api clean uninstall
