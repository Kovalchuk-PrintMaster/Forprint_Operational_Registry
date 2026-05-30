from forprint_operational_registry.dto.errors import (
    KNOWN_ERROR_CODES,
    KNOWN_WARNING_CODES,
    OperationalErrorCode,
    OperationalWarningCode,
)
from forprint_operational_registry.dto.results import (
    OperationalCommandResult,
    OperationalResultStatus,
)


def test_known_error_codes_exist() -> None:
    assert OperationalErrorCode.INVALID_TRANSITION.value in KNOWN_ERROR_CODES
    assert OperationalErrorCode.BLOCKED_BY_ACTIVE_BLOCKER.value in KNOWN_ERROR_CODES
    assert OperationalErrorCode.FORBIDDEN_FOREIGN_OWNERSHIP.value in KNOWN_ERROR_CODES


def test_known_warning_codes_exist() -> None:
    assert OperationalWarningCode.MISSING_CALCULATION_REFERENCE.value in KNOWN_WARNING_CODES
    assert OperationalWarningCode.WAITING_PAYMENT_REFERENCE.value in KNOWN_WARNING_CODES


def test_operational_command_result_preserves_correlation_and_idempotency() -> None:
    result = OperationalCommandResult(
        result_id="result_001",
        command_id="cmd_001",
        correlation_id="corr_001",
        idempotency_key="idem_001",
        status=OperationalResultStatus.APPLIED.value,
        entity_type="order",
        entity_id="order_001",
    )

    assert result.command_id == "cmd_001"
    assert result.correlation_id == "corr_001"
    assert result.idempotency_key == "idem_001"
