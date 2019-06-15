.PHONY: env install help server test test-changes test-loop

VENV=venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest
PTW=$(VENV)/bin/ptw

help:
	@echo "Toptal Calorie Tracker Backend"
	@echo "### Commands ###"
	@echo "env"
	@echo "install"
	@echo "server"
	@echo "test"
	@echo "test-changes"
	@echo "test-loop"

env:
	test -d $(VENV) || virtualenv $(VENV) -p python3
	@echo "\`$(VENV)\` is virtualenv"

install: env
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

server:
	$(PYTHON) create_app.py

test:
	$(PYTEST) -n4 tests/

test-changes:
	$(PYTEST) --testmon tests/

test-loop:
	$(PTW) --onpass "say passed" --onfail "say failed" -- --testmon

test-user:
	$(PYTEST) tests/resources/test_user_resource.py tests/models/test_user_model.py
