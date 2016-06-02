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

run:
	$(PYTHON) lift/main.py $(TARGET) && $(PYTHON) tube/main.py a.out

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) tests

lint:
	$(LINT) tests/* src/* 

doc:
	$(SPHINX) -b html docs/source docs/build

.PHONY: install, test, lint, doc, run
