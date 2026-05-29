PYTHON ?= .venv_operational_registry/bin/python
PIP ?= .venv_operational_registry/bin/pip

.PHONY: install test lint check check-report format clean

install:
	python3.11 -m venv .venv_operational_registry
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check app tests scripts

check: lint test

check-report:
	$(PYTHON) scripts/run_operational_registry_checks.py

format:
	$(PYTHON) -m ruff check app tests scripts --fix
	$(PYTHON) -m ruff format app tests scripts

clean:
	rm -rf reports
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +