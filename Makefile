ifeq ($(OS),Windows_NT)
	PYTHON = env/Scripts/python
    PIP = env/Scripts/pip
    PYTEST = env/Scripts/py.test
    LINT = env/Scripts/pylint
    SPHINX = env/Scripts/sphinx-build  
else
	PYTHON = env/bin/python
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

run:
	$(PYTHON) src/main.py $(filter-out $@,$(MAKECMDGOALS))

.PHONY: install, test, lint, doc, run
