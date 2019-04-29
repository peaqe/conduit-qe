# conduit-qe

`conduit-qe` is the testing tool for the `rhsm-conduit` project.

## Getting Started

conduit-qe can be installed in two ways. The first one is recommended for
everyone who is interested on just running the functional tests. The second are
for people interested on contribute by helping improving either the automation
framework or the test cases.

This project uses `pipenv` to manage the Python environment. There is also a
`Makefile` for convenience and automation.  

To install conduit-qe if only running tests do the following:

```
pipenv install
```

To set the project up for test development and running tests do the following:

```
pipenv install --dev
```

Afterwards you can activate the virtual environment by running:

```
pipenv shell
```

## Running the API Tests

After starting the virtual environment, the `rhsm-conduit` API tests
can be easily run by calling as it follows:

```
py.test -v conduitqe/tests/api/
```
