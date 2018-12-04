.PHONY: help server test

help:
	@echo "Toptal Calorie Tracker Backend"
	@echo "### Commands ###"
	@echo "env"
	@echo "server"
	@echo "tests"

server:
	python create_app.py

test:
	python -m nose -s --verbosity=3 tests/
