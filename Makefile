PYTEST_OPTIONS = -vvv

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
	pipenv run py.test tests

test-api:
	pipenv run py.test $(PYTEST_OPTIONS) conduitqe/tests/api/v1


test-coverage:
	pipenv run py.test --verbose --cov-report term --cov=conduitqe --cov=tests tests

docs:
	scripts/gendocs.sh

clean:
	rm -f *.log
	rm -f *.xml
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

uninstall:
	pipenv --rm || true

.PHONY: all install install-dev lint test test-coverage test-api docs clean uninstall
