PYTHON ?= .venv_operational_registry/bin/python
PIP ?= .venv_operational_registry/bin/pip

.PHONY: install test lint lint-fix check check-report status-report format 
	clean client-card-preview blueprint-pull blueprint-check blueprint-sync-directives 
	coordination-check coordination-fix module-policy-check
	data-foundation-preview order-preview workflow-preview payment-preview 
	material-requirement-preview alert-preview operational-report-preview

install:
	python3.11 -m venv .venv_operational_registry
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint-fix:
	$(PYTHON) -m ruff check app tests scripts --fix

lint:
	$(PYTHON) -m ruff check app tests scripts

status-report:
	$(PYTHON) scripts/export_module_status.py

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
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +

client-card-preview:
	$(PYTHON) scripts/client_card_preview.py

blueprint-pull:
	@echo "DEFERRED: Blueprint pull is not wired for this module yet."

blueprint-check:
	@echo "DEFERRED: Blueprint check is not wired for this module yet."

blueprint-sync-directives:
	@echo "DEFERRED: Blueprint directive sync is not wired for this module yet."

coordination-check:
	@test -f coordination/status/current_status.yaml
	@test -f coordination/status/current_status.md
	@test -f coordination/reports/index.yaml
	@echo "✅ Coordination files exist."

coordination-fix:
	@echo "DEFERRED: automatic coordination fix is not implemented yet."

module-policy-check:
	$(PYTHON) scripts/run_operational_registry_checks.py

data-foundation-preview:
	$(PYTHON) scripts/data_foundation_preview.py

order-preview:
	$(PYTHON) scripts/order_workflow_preview.py order

workflow-preview:
	$(PYTHON) scripts/order_workflow_preview.py workflow

payment-preview:
	$(PYTHON) scripts/order_workflow_preview.py payment

material-requirement-preview:
	$(PYTHON) scripts/order_workflow_preview.py material

alert-preview:
	$(PYTHON) scripts/order_workflow_preview.py alert

operational-report-preview:
	$(PYTHON) scripts/order_workflow_preview.py report