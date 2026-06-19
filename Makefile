PYTHON ?= .venv_operational_registry/bin/python
PIP ?= .venv_operational_registry/bin/pip

BLUEPRINT_ROOT ?= /srv/software_development/forprint-project/forprint_system_blueprint
ACTIVE_PROMPT_MODULE ?= forprint_operational_registry
BLUEPRINT_PROMPTS_ROOT ?= $(BLUEPRINT_ROOT)/coordination/outgoing_prompts
BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR ?= $(BLUEPRINT_PROMPTS_ROOT)/$(ACTIVE_PROMPT_MODULE)/approved
ACTIVE_PROMPT_LOCAL_DIR ?= coordination/outgoing_prompts/approved

PACKET ?= coordination/completion_packets/examples/local_launch_readiness_v0_1.yaml

.PHONY: install test lint lint-fix format check check-report status-report
.PHONY: clean report-clean
.PHONY: blueprint-paths-check blueprint-pull blueprint-check blueprint-sync-directives blueprint-sync
.PHONY: blueprint-instruction-list blueprint-instruction-check blueprint-instruction-sync
.PHONY: blueprint-standards-list blueprint-standards-check blueprint-standards-sync
.PHONY: blueprint-prompts-list blueprint-prompts-sync blueprint-prompts-check blueprint-prompts prompt-read
.PHONY: module-start module-sync module-validate module-finish
.PHONY: coordination-check coordination-fix module-policy-check governance-check
.PHONY: completion-packet-check completion-packet-validate completion-packet-apply
.PHONY: client-card-preview data-foundation-preview order-preview workflow-preview
.PHONY: payment-preview material-requirement-preview alert-preview operational-report-preview
.PHONY: dictionary-mapping-preview

# ==============================================================================
# Середовище
# ==============================================================================

# Команда: make install
# Що робить: створює локальне Python 3.11 venv та встановлює dev-залежності.
# Очікуваний результат: .venv_operational_registry існує, модуль встановлено в editable dev mode.
install:
	python3.11 -m venv .venv_operational_registry
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

# ==============================================================================
# Базова локальна валідація
# ==============================================================================

# Команда: make test
# Що робить: запускає повний pytest-набір.
# Очікуваний результат: усі тести проходять.
test:
	$(PYTHON) -m pytest -q

# Команда: make lint
# Що робить: запускає Ruff lint без автоматичних змін.
# Очікуваний результат: немає lint-помилок у app, tests, scripts.
lint:
	$(PYTHON) -m ruff check app tests scripts

# Команда: make lint-fix
# Що робить: запускає Ruff lint з автоматичним виправленням безпечних помилок.
# Очікуваний результат: fixable lint-помилки виправлені автоматично.
lint-fix:
	$(PYTHON) -m ruff check app tests scripts --fix

# Команда: make format
# Що робить: форматує app, tests, scripts через Ruff formatter.
# Очікуваний результат: Python-код відформатований однаково.
format:
	$(PYTHON) -m ruff format app tests scripts

# Команда: make check
# Що робить: запускає lint і tests як основний локальний validation gate.
# Очікуваний результат: lint OK і pytest OK.
check: lint test

# Команда: make check-report
# Що робить: запускає структурований Operational Registry check-report.
# Очікуваний результат: усі module policy, boundary, preview і coordination checks мають статус OK.
check-report:
	$(PYTHON) scripts/run_operational_registry_checks.py

# Команда: make status-report
# Що робить: експортує поточний module status JSON report.
# Очікуваний результат: локально створено reports/operational_registry_module_status.json.
status-report:
	$(PYTHON) scripts/export_module_status.py

# ==============================================================================
# Очищення
# ==============================================================================

# Команда: make clean
# Що робить: видаляє generated reports і локальні Python/tool caches.
# Очікуваний результат: службовий локальний шум прибрано.
clean:
	rm -rf reports
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +

# Команда: make report-clean
# Що робить: прибирає generated report diffs, якщо ці файли tracked; якщо їх немає або вони untracked — не падає.
# Очікуваний результат: generated report diffs не заважають git status.
report-clean:
	git restore -- reports/operational_registry_check_report.json reports/operational_registry_check_report.md reports/operational_registry_module_status.json 2>/dev/null || true
	@echo "✅ Generated reports restored/cleaned."

# ==============================================================================
# Blueprint paths і базова синхронізація
# ==============================================================================

# Команда: make blueprint-paths-check
# Що робить: перевіряє наявність потрібних локальних директорій Blueprint.
# Очікуваний результат: Blueprint root, coordination, instruction_intake, standards і outgoing_prompts доступні.
blueprint-paths-check:
	@echo "== Blueprint paths check =="
	@test -d "$(BLUEPRINT_ROOT)" || (echo "Missing Blueprint root: $(BLUEPRINT_ROOT)"; exit 1)
	@test -d "$(BLUEPRINT_ROOT)/coordination" || (echo "Missing Blueprint coordination directory"; exit 1)
	@test -d "$(BLUEPRINT_ROOT)/coordination/instruction_intake" || (echo "Missing Blueprint instruction intake directory"; exit 1)
	@test -d "$(BLUEPRINT_ROOT)/coordination/standards" || (echo "Missing Blueprint standards directory"; exit 1)
	@test -d "$(BLUEPRINT_PROMPTS_ROOT)" || (echo "Missing Blueprint outgoing prompts root: $(BLUEPRINT_PROMPTS_ROOT)"; exit 1)
	@test -d "$(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)" || (echo "Missing Blueprint module approved prompt directory: $(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)"; exit 1)
	@echo "✅ Blueprint paths are available."

# Команда: make blueprint-pull
# Що робить: після перевірки шляхів виконує git pull --ff-only у Blueprint repo.
# Очікуваний результат: локальний Blueprint оновлений або безпечно зупинений, якщо потрібен non-fast-forward.
blueprint-pull: blueprint-paths-check
	git -C $(BLUEPRINT_ROOT) pull --ff-only

# Команда: make blueprint-sync-directives
# Що робить: placeholder для майбутньої синхронізації Blueprint directives.
# Очікуваний результат: зараз явно показує DEFERRED і не ламає workflow.
blueprint-sync-directives:
	@echo "DEFERRED: Blueprint directive sync is not wired for this module yet."

# ==============================================================================
# Blueprint instruction intake
# ==============================================================================

# Команда: make blueprint-instruction-list
# Що робить: показує Blueprint instruction intake sources та їх priority order.
# Очікуваний результат: оператор бачить ієрархію джерел інструкцій для модуля.
blueprint-instruction-list:
	$(PYTHON) scripts/list_blueprint_instruction_sources.py

# Команда: make blueprint-instruction-check
# Що робить: перевіряє, що локальний Blueprint instruction packet читається і boundary-safe.
# Очікуваний результат: instruction packet валідний і посилається на актуальний Blueprint commit.
blueprint-instruction-check:
	$(PYTHON) scripts/check_blueprint_instruction_intake.py

# Команда: make blueprint-instruction-sync
# Що робить: синхронізує локальний snapshot Blueprint instruction packet.
# Очікуваний результат: semantic changes записуються; повторні timestamp-only runs не створюють dirty diff.
blueprint-instruction-sync:
	$(PYTHON) scripts/sync_blueprint_instruction_packet.py

# ==============================================================================
# Blueprint standards visibility
# ==============================================================================

# Команда: make blueprint-standards-list
# Що робить: показує Blueprint standards, видимі модулю.
# Очікуваний результат: оператор бачить active/advisory standards і alignment level.
blueprint-standards-list:
	$(PYTHON) scripts/list_blueprint_standards.py

# Команда: make blueprint-standards-check
# Що робить: перевіряє локальну видимість Blueprint standards.
# Очікуваний результат: standards index і local snapshot читаються, advisory semantics explicit.
blueprint-standards-check:
	$(PYTHON) scripts/check_blueprint_standards.py

# Команда: make blueprint-standards-sync
# Що робить: синхронізує локальний Blueprint standards snapshot.
# Очікуваний результат: semantic changes записуються; повторні timestamp-only runs не створюють dirty diff.
blueprint-standards-sync:
	$(PYTHON) scripts/sync_blueprint_standards.py

# ==============================================================================
# Blueprint outgoing prompts
# ==============================================================================

# Команда: make blueprint-prompts-list
# Що робить: показує approved Blueprint outgoing prompt markdown files тільки для цього модуля.
# Очікуваний результат: видно актуальний approved prompt з Blueprint.
blueprint-prompts-list:
	@echo "== Blueprint approved prompts for $(ACTIVE_PROMPT_MODULE) =="
	@test -d "$(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)" || (echo "Missing Blueprint approved prompt directory: $(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)"; exit 1)
	@find "$(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)" -maxdepth 1 -type f -name "*.md" | sort

# Команда: make blueprint-prompts-sync
# Що робить: копіює approved Blueprint outgoing prompt markdown files у локальну coordination-директорію модуля.
# Очікуваний результат: coordination/outgoing_prompts/approved містить актуальний approved prompt markdown.
blueprint-prompts-sync:
	@echo "== Sync Blueprint approved prompts for $(ACTIVE_PROMPT_MODULE) =="
	@test -d "$(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)" || (echo "Missing Blueprint approved prompt directory: $(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)"; exit 1)
	@files="$$(find "$(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)" -maxdepth 1 -type f -name "*.md" | sort)"; if [ -z "$$files" ]; then echo "No approved Blueprint prompt markdown files found in $(BLUEPRINT_ACTIVE_PROMPT_SOURCE_DIR)"; exit 1; fi; mkdir -p "$(ACTIVE_PROMPT_LOCAL_DIR)"; find "$(ACTIVE_PROMPT_LOCAL_DIR)" -maxdepth 1 -type f -name "*.md" -delete; for file in $$files; do cp "$$file" "$(ACTIVE_PROMPT_LOCAL_DIR)/$$(basename "$$file")"; done
	@echo "✅ Blueprint approved prompt files synced to $(ACTIVE_PROMPT_LOCAL_DIR)"

# Команда: make blueprint-prompts-check
# Що робить: перевіряє, що локальний approved prompt існує і містить очікувані make-first/readiness маркери.
# Очікуваний результат: активний локальний prompt присутній і відповідає local_operator_command_query_readiness_v0_1.
blueprint-prompts-check:
	@echo "== Check local approved Blueprint prompt =="
	@test -d "$(ACTIVE_PROMPT_LOCAL_DIR)" || (echo "Missing $(ACTIVE_PROMPT_LOCAL_DIR). Run make blueprint-prompts-sync"; exit 1)
	@find "$(ACTIVE_PROMPT_LOCAL_DIR)" -maxdepth 1 -type f -name "*.md" | grep -q . || (echo "No active approved prompt markdown files found in $(ACTIVE_PROMPT_LOCAL_DIR)"; exit 1)
	@grep -R -E "local_operator_command_query_readiness_v0_1|make-first|module-start|module-validate" "$(ACTIVE_PROMPT_LOCAL_DIR)" >/dev/null || (echo "Active prompt files do not mention expected readiness/make-first workflow terms"; exit 1)
	@echo "✅ Active approved Blueprint prompt files are available."

# Команда: make blueprint-prompts
# Що робить: виконує list, sync і check для Blueprint outgoing prompts.
# Очікуваний результат: active approved prompt видимий, синхронізований і валідований локально.
blueprint-prompts: blueprint-prompts-list blueprint-prompts-sync blueprint-prompts-check
	@echo "✅ Blueprint prompts workflow completed."

# Команда: make prompt-read
# Що робить: показує локальні approved prompt-файли і перші 220 рядків їхнього змісту.
# Очікуваний результат: assistant/operator може прочитати активний prompt без ручного пошуку у Blueprint.
prompt-read:
	@echo "== Active approved Blueprint prompt files =="
	@test -d "$(ACTIVE_PROMPT_LOCAL_DIR)" || (echo "Missing $(ACTIVE_PROMPT_LOCAL_DIR). Run make blueprint-prompts-sync"; exit 1)
	@find "$(ACTIVE_PROMPT_LOCAL_DIR)" -maxdepth 1 -type f -name "*.md" | sort
	@echo ""
	@echo "== Active approved Blueprint prompt content preview =="
	@find "$(ACTIVE_PROMPT_LOCAL_DIR)" -maxdepth 1 -type f -name "*.md" | sort | while read file; do echo ""; echo "----- $$file -----"; sed -n '1,220p' "$$file"; done

# ==============================================================================
# Blueprint aggregate workflow
# ==============================================================================

# Команда: make blueprint-check
# Що робить: перевіряє instruction intake, standards visibility і наявність active prompt.
# Очікуваний результат: усі Blueprint-facing local checks проходять.
blueprint-check: blueprint-instruction-check blueprint-standards-check blueprint-prompts-check
	@echo "✅ Blueprint checks completed."

# Команда: make blueprint-sync
# Що робить: pull Blueprint, directives placeholder, sync/check instruction intake, standards і approved prompts.
# Очікуваний результат: локальний модуль має актуальну Blueprint visibility і актуальний approved prompt.
blueprint-sync: blueprint-pull blueprint-sync-directives blueprint-instruction-list blueprint-instruction-sync blueprint-instruction-check blueprint-standards-list blueprint-standards-sync blueprint-standards-check blueprint-prompts
	@echo "✅ Blueprint sync completed."

# ==============================================================================
# Coordination і module policy
# ==============================================================================

# Команда: make coordination-check
# Що робить: перевіряє наявність обов’язкових coordination-файлів.
# Очікуваний результат: current_status.yaml, current_status.md і reports index існують.
coordination-check:
	@test -f coordination/status/current_status.yaml
	@test -f coordination/status/current_status.md
	@test -f coordination/reports/index.yaml
	@echo "✅ Coordination files exist."

# Команда: make coordination-fix
# Що робить: reserved placeholder для майбутнього автоматичного ремонту coordination records.
# Очікуваний результат: зараз показує DEFERRED і не змінює файли.
coordination-fix:
	@echo "DEFERRED: automatic coordination fix is not implemented yet."

# Команда: make module-policy-check
# Що робить: запускає той самий structured Operational Registry check-report, що використовується governance workflow.
# Очікуваний результат: module boundaries, docs, previews і coordination checks мають статус OK.
module-policy-check:
	$(PYTHON) scripts/run_operational_registry_checks.py

# ==============================================================================
# Make Command Standard v0.2 — module workflow
# ==============================================================================

# Команда: make module-start
# Що робить: виконує required make-first startup workflow перед будь-якою основною реалізацією.
# Очікуваний результат: Blueprint синхронізовано, approved prompt читається, coordination існує, current status показано.
module-start: blueprint-sync coordination-check prompt-read
	@echo "== Current module status =="
	@sed -n '1,140p' coordination/status/current_status.yaml
	@echo "✅ Module start completed. Active prompt is ready for make-first workflow."

# Команда: make module-sync
# Що робить: оновлює Blueprint-facing state модуля без повної локальної валідації.
# Очікуваний результат: instruction packet, standards snapshot і approved prompt актуальні.
module-sync: blueprint-sync
	@echo "✅ Module sync completed."

# Команда: make module-validate
# Що робить: запускає completion packet validation, check-report, lint/tests і governance-check.
# Очікуваний результат: модуль зелений перед або після checkpoint.
module-validate: completion-packet-check check-report check governance-check
	@echo "✅ Module validation completed."

# Команда: make module-finish
# Що робить: запускає фінальний module validation workflow для вибраного PACKET.
# Очікуваний результат: вибраний completion packet валідний і всі module validation checks проходять.
module-finish: module-validate
	@echo "✅ Module finish checks completed. Review git diff before commit."

# ==============================================================================
# Completion packets
# ==============================================================================

# Команда: make completion-packet-check
# Що робить: перевіряє вибраний completion packet зі змінної PACKET.
# Очікуваний результат: packet schema і required boundary/check fields валідні.
completion-packet-check:
	$(PYTHON) scripts/validate_completion_packet.py $(PACKET)

# Команда: make completion-packet-validate
# Що робить: explicit alias для перевірки вибраного completion packet.
# Очікуваний результат: вибраний completion packet валідний.
completion-packet-validate:
	$(PYTHON) scripts/validate_completion_packet.py $(PACKET)

# Команда: make completion-packet-apply
# Що робить: застосовує вибраний completion packet до report/status coordination files.
# Очікуваний результат: report/index/status створені або оновлені idempotently.
completion-packet-apply:
	$(PYTHON) scripts/apply_completion_packet.py $(PACKET)

# ==============================================================================
# Локальні previews
# ==============================================================================

# Команда: make client-card-preview
# Що робить: показує safe local ClientAccount card terminal preview.
# Очікуваний результат: preview рендериться без external integrations.
client-card-preview:
	$(PYTHON) scripts/client_card_preview.py

# Команда: make data-foundation-preview
# Що робить: показує safe local data foundation terminal preview.
# Очікуваний результат: data foundation concepts успішно рендеряться.
data-foundation-preview:
	$(PYTHON) scripts/data_foundation_preview.py

# Команда: make order-preview
# Що робить: показує safe local order projection preview.
# Очікуваний результат: order projection можна переглянути в терміналі.
order-preview:
	$(PYTHON) scripts/order_workflow_preview.py order

# Команда: make workflow-preview
# Що робить: показує safe local workflow projection preview.
# Очікуваний результат: workflow state можна переглянути в терміналі.
workflow-preview:
	$(PYTHON) scripts/order_workflow_preview.py workflow

# Команда: make payment-preview
# Що робить: показує safe local payment reference/projection preview.
# Очікуваний результат: payment references видимі без ownership над accounting truth.
payment-preview:
	$(PYTHON) scripts/order_workflow_preview.py payment

# Команда: make material-requirement-preview
# Що робить: показує safe local material requirement preview.
# Очікуваний результат: material requirement references видимі без ownership над warehouse stock truth.
material-requirement-preview:
	$(PYTHON) scripts/order_workflow_preview.py material

# Команда: make alert-preview
# Що робить: показує safe local operational alert preview.
# Очікуваний результат: local alert projection можна переглянути в терміналі.
alert-preview:
	$(PYTHON) scripts/order_workflow_preview.py alert

# Команда: make operational-report-preview
# Що робить: показує safe local operational report preview.
# Очікуваний результат: operator може переглянути offline operational summary output.
operational-report-preview:
	$(PYTHON) scripts/order_workflow_preview.py report

# Команда: make dictionary-mapping-preview
# Що робить: показує local Library dictionary mapping preview.
# Очікуваний результат: local enum/status mappings можна переглянути без live Library integration.
dictionary-mapping-preview:
	$(PYTHON) scripts/dictionary_mapping_preview.py

# ==============================================================================
# Governance
# ==============================================================================

# Команда: make governance-check
# Що робить: запускає module governance workflow: Blueprint pull/checks, module policy check, coordination check і status export.
# Очікуваний результат: governance validation проходить; directive sync може залишатися явно DEFERRED.
governance-check:
	@echo "== ForPrint Operational Registry governance check =="
	$(MAKE) blueprint-pull
	$(MAKE) blueprint-check
	$(MAKE) blueprint-sync-directives
	$(MAKE) blueprint-instruction-check
	$(MAKE) blueprint-standards-check
	$(MAKE) module-policy-check
	$(MAKE) coordination-check
	$(MAKE) status-report