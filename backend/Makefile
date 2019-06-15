.PHONY: install help server test

VENV=venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip

help:
	@echo "Toptal Calorie Tracker Backend"
	@echo "### Commands ###"
	@echo "env"
	@echo "server"
	@echo "test"

env:
	test -d $(VENV) || virtualenv $(VENV) -p python3
	@echo "\`$(VENV)\` is virtualenv"

install: env
	$(PIP) install -r requirements.txt

server:
	$(PYTHON) create_app.py

test:
	$(PYTHON) -m pytest -n4 tests/

test-user:
	$(PYTHON) -m pytest tests/resources/test_user_resource.py
# 	$(PYTHON) -m pytest tests/models/test_user_model.py
