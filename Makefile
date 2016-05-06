ifeq ($(OS),Windows_NT)
    PIP = env/Scripts/pip
    PYTEST = env/Scripts/py.test
    LINT = env/Scripts/pylint
    SPHINX = env/Scripts/sphinx-build  
else
    PIP = env/bin/pip
    PYTEST = env/bin/py.test
    LINT = env/bin/pylint
    SPHINX = env/bin/sphinx-build  
endif

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) tests

lint:
	$(LINT) tests/* src/*

doc:
	$(SPHINX) -b html docs/source docs/build

.PHONY: install, test, lint, doc
