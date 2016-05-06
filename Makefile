PIP = env/bin/pip
PYTEST = env/bin/py.test
LINT = env/bin/pylint
SPHINX = env/bin/sphinx-build

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) tests

lint:
	$(LINT) tests/* src/*

doc:
	$(SPHINX) -b html doc/source doc/build

.PHONY: install, test, lint, doc
