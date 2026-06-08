"""Order / workflow / projection foundation models.

Checkpoint A adds flexible operational order and reference concepts only.

No Calculator runtime integration.
No Library runtime integration.
No Accounting runtime integration.
No Warehouse runtime integration.
No production API.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

ORDER_STATUSES: tuple[str, ...] = (
    "draft",
    "new",
    "needs_review",
    "quote_pending",
    "quote_accepted",
    "payment_reference_pending",
    "payment_reference_confirmed",
    "in_workflow",
    "in_production",
    "completed",
    "cancelled",
    "blocked",
    "unknown",
)

PAYMENT_PROJECTION_STATUSES: tuple[str, ...] = (
    "not_invoiced",
    "invoice_reference_pending",
    "unpaid",
    "partially_paid",
    "paid_reference_confirmed",
    "overdue",
    "cancelled",
    "unknown",
)

PRODUCTION_STATUSES: tuple[str, ...] = (
    "not_started",
    "waiting_prepress",
    "ready_for_production",
    "in_production",
    "ready_for_pickup",
    "completed",
    "blocked",
    "cancelled",
    "unknown",
)

WORKFLOW_STATUSES: tuple[str, ...] = (
    "not_started",
    "ready",
    "in_progress",
    "blocked",
    "waiting_external_contractor",
    "completed",
    "cancelled",
    "late",
    "manual_review_required",
    "unknown",
)

PRODUCT_SERVICE_RESOLUTION_STATUSES: tuple[str, ...] = (
    "draft_display_only",
    "library_reference_pending",
    "library_reference_confirmed",
    "ambiguous_manual_review_required",
    "deprecated_reference",
    "unknown",
)

CALCULATOR_REFERENCE_VALIDATION_STATUSES: tuple[str, ...] = (
    "not_validated",
    "reference_received",
    "schema_version_pending",
    "validation_passed",
    "validation_failed",
    "unknown",
)

FORBIDDEN_ORDER_PAYLOAD_KEYS: tuple[str, ...] = (
    "calculator_formula",
    "pricing_rule",
    "price_calculation_logic",
    "accounting_posting",
    "one_c_write_result",
    "warehouse_stock_truth",
    "warehouse_reservation_truth",
    "library_canonical_product_definition",
    "telegram_runtime_ui",
    "crm_dashboard_state",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Freeze mapping to avoid accidental mutation."""

    return MappingProxyType(dict(value or {}))


def ensure_in(value: str, allowed: tuple[str, ...], field_name: str) -> None:
    """Validate local draft enum value."""

    if value not in allowed:
        raise ValueError(f"Unknown {field_name}: {value}")


def ensure_no_forbidden_payload_keys(payload: Mapping[str, Any]) -> None:
    """Reject obvious foreign-domain ownership markers."""

    forbidden_keys = set(payload).intersection(FORBIDDEN_ORDER_PAYLOAD_KEYS)
    if forbidden_keys:
        raise ValueError(
            "Operational order foundation must not own foreign-domain truth. "
            f"Forbidden payload keys: {sorted(forbidden_keys)}"
        )


@dataclass(slots=True)
class OperationalOrder:
    """Internal ForPrint operational order record.

    Order belongs to ClientAccount.
    ClientGroup is analytics/grouping only.
    Calculator refs are references only.
    Operational Registry must not calculate final prices.
    Accounting payment truth is referenced, not owned here.
    """

    order_id: str
    client_account_id: str
    client_group_id: str | None = None
    source_request_id: str | None = None
    calculator_output_package_id: str | None = None
    calculator_calculation_id: str | None = None
    calculator_quote_id: str | None = None
    calculator_order_draft_id: str | None = None
    status: str = "new"
    order_date: datetime = field(default_factory=utc_now)
    planned_due_at: datetime | None = None
    confirmed_due_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    currency: str = "UAH"
    total_amount_planned: float | None = None
    total_amount_confirmed: float | None = None
    payment_status: str = "not_invoiced"
    production_status: str = "not_started"
    workflow_status: str = "not_started"
    source_system: str = "manual"
    source_ref: str | None = None
    raw_source_payload: Mapping[str, Any] = field(default_factory=dict)
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        if not self.currency:
            raise ValueError("currency is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        ensure_in(self.status, ORDER_STATUSES, "status")
        ensure_in(self.payment_status, PAYMENT_PROJECTION_STATUSES, "payment_status")
        ensure_in(self.production_status, PRODUCTION_STATUSES, "production_status")
        ensure_in(self.workflow_status, WORKFLOW_STATUSES, "workflow_status")
        ensure_no_forbidden_payload_keys(self.raw_source_payload)

        if self.total_amount_planned is not None and self.total_amount_planned < 0:
            raise ValueError("total_amount_planned must not be negative")

        if self.total_amount_confirmed is not None and self.total_amount_confirmed < 0:
            raise ValueError("total_amount_confirmed must not be negative")

        self.raw_source_payload = freeze_mapping(self.raw_source_payload)


@dataclass(slots=True)
class OperationalOrderLine:
    """Product/service line in an operational order.

    Display name is not canonical truth.
    Library IDs become canonical when available.
    Until Library is ready, raw/display names and draft refs are preserved.
    """

    order_line_id: str
    order_id: str
    line_no: int
    product_or_service_display_name: str
    quantity: float
    unit: str
    library_product_id: str | None = None
    library_service_id: str | None = None
    library_material_id: str | None = None
    raw_product_or_service_name: str | None = None
    unit_price_planned: float | None = None
    line_total_planned: float | None = None
    line_total_confirmed: float | None = None
    calculator_line_ref: str | None = None
    calculator_operation_ref: str | None = None
    status: str = "draft"
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.order_line_id:
            raise ValueError("order_line_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if self.line_no <= 0:
            raise ValueError("line_no must be positive")

        if not self.product_or_service_display_name:
            raise ValueError("product_or_service_display_name is required")

        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

        if not self.unit:
            raise ValueError("unit is required")

        ensure_in(self.status, ORDER_STATUSES, "status")

        for field_name, value in (
            ("unit_price_planned", self.unit_price_planned),
            ("line_total_planned", self.line_total_planned),
            ("line_total_confirmed", self.line_total_confirmed),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{field_name} must not be negative")


@dataclass(slots=True)
class CalculatorOutputPackageReference:
    """Reference to future Calculator output package.

    This does not copy Calculator formulas or pricing rules.
    """

    calculator_reference_id: str
    calculator_output_package_id: str
    order_id: str | None = None
    source_system: str = "calculator_engine"
    calculator_calculation_id: str | None = None
    quote_draft_id: str | None = None
    order_draft_id: str | None = None
    schema_version: str | None = None
    received_at: datetime | None = None
    raw_payload_ref: str | None = None
    validation_status: str = "not_validated"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.calculator_reference_id:
            raise ValueError("calculator_reference_id is required")

        if not self.calculator_output_package_id:
            raise ValueError("calculator_output_package_id is required")

        if self.source_system != "calculator_engine":
            raise ValueError("source_system must be calculator_engine")

        ensure_in(
            self.validation_status,
            CALCULATOR_REFERENCE_VALIDATION_STATUSES,
            "validation_status",
        )


@dataclass(slots=True)
class ProductServiceReference:
    """Flexible reference to future ForPrint Library catalog entity."""

    product_service_reference_id: str
    display_name: str
    order_line_id: str | None = None
    library_entity_type: str | None = None
    library_entity_id: str | None = None
    raw_name: str | None = None
    source_system: str = "manual"
    resolution_status: str = "draft_display_only"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.product_service_reference_id:
            raise ValueError("product_service_reference_id is required")

        if not self.display_name:
            raise ValueError("display_name is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        ensure_in(
            self.resolution_status,
            PRODUCT_SERVICE_RESOLUTION_STATUSES,
            "resolution_status",
        )

        if self.resolution_status == "library_reference_confirmed" and not self.library_entity_id:
            raise ValueError(
                "library_entity_id is required when resolution_status is "
                "library_reference_confirmed"
            )


MATERIAL_REQUIREMENT_STATUSES: tuple[str, ...] = (
    "planned",
    "library_reference_pending",
    "warehouse_reference_pending",
    "reserved_reference_pending",
    "confirmed",
    "fulfilled",
    "cancelled",
    "unknown",
)

PAYMENT_VISIBILITY_STATUSES: tuple[str, ...] = (
    "not_invoiced",
    "invoice_reference_pending",
    "unpaid",
    "partially_paid",
    "paid_reference_confirmed",
    "overdue",
    "cancelled",
    "unknown",
)

CONTRACTOR_RESOLUTION_STATUSES: tuple[str, ...] = (
    "display_only",
    "client_account_reference_pending",
    "client_account_reference_confirmed",
    "external_reference_pending",
    "manual_review_required",
)

DEADLINE_TYPES: tuple[str, ...] = (
    "order_due",
    "stage_due",
    "payment_due",
    "material_required_by",
    "manual_review_due",
)

DEADLINE_STATUSES: tuple[str, ...] = (
    "active",
    "warning",
    "late",
    "completed",
    "cancelled",
    "unknown",
)


@dataclass(slots=True)
class MaterialRequirement:
    """Planned material need.

    This is not warehouse stock truth.
    Operational Registry stores planning/projection only.
    """

    material_requirement_id: str
    order_id: str
    material_display_name: str
    quantity_planned: float
    unit: str
    order_line_id: str | None = None
    library_material_id: str | None = None
    raw_material_name: str | None = None
    quantity_confirmed: float | None = None
    source_type: str = "manual"
    source_ref: str | None = None
    requirement_status: str = "planned"
    required_by: datetime | None = None
    warehouse_reference: str | None = None
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.material_requirement_id:
            raise ValueError("material_requirement_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.material_display_name:
            raise ValueError("material_display_name is required")

        if self.quantity_planned <= 0:
            raise ValueError("quantity_planned must be positive")

        if self.quantity_confirmed is not None and self.quantity_confirmed < 0:
            raise ValueError("quantity_confirmed must not be negative")

        if not self.unit:
            raise ValueError("unit is required")

        if not self.source_type:
            raise ValueError("source_type is required")

        ensure_in(
            self.requirement_status,
            MATERIAL_REQUIREMENT_STATUSES,
            "requirement_status",
        )

    @property
    def is_unresolved(self) -> bool:
        """Return whether material requirement is still unresolved."""

        return self.requirement_status in {
            "planned",
            "library_reference_pending",
            "warehouse_reference_pending",
            "reserved_reference_pending",
            "unknown",
        }


@dataclass(slots=True)
class PaymentProjection:
    """Operational payment/debt visibility.

    Accounting Registry remains owner of accounting sync and 1C posting.
    Operational Registry stores projection/read model only.
    """

    payment_projection_id: str
    order_id: str
    client_account_id: str
    total_amount: float
    paid_amount: float
    currency: str = "UAH"
    accounting_invoice_ref: str | None = None
    accounting_payment_ref: str | None = None
    one_c_document_ref: str | None = None
    payment_status: str = "not_invoiced"
    due_date: datetime | None = None
    last_payment_seen_at: datetime | None = None
    source_system: str = "manual"
    sync_confidence: str = "unknown"
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.payment_projection_id:
            raise ValueError("payment_projection_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        if self.total_amount < 0:
            raise ValueError("total_amount must not be negative")

        if self.paid_amount < 0:
            raise ValueError("paid_amount must not be negative")

        if self.paid_amount > self.total_amount:
            raise ValueError("paid_amount must not exceed total_amount")

        if not self.currency:
            raise ValueError("currency is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        ensure_in(self.payment_status, PAYMENT_VISIBILITY_STATUSES, "payment_status")

    @property
    def unpaid_amount(self) -> float:
        """Calculate unpaid amount for operational visibility."""

        return round(self.total_amount - self.paid_amount, 2)


@dataclass(frozen=True, slots=True)
class WorkflowStageTemplate:
    """Stage definition inside WorkflowTemplate."""

    stage_code: str
    stage_name: str
    default_order: int
    default_duration_minutes: int | None = None
    responsible_role: str | None = None
    default_contractor_type: str | None = None
    can_be_manual_override: bool = True
    is_required: bool = True

    def __post_init__(self) -> None:
        if not self.stage_code:
            raise ValueError("stage_code is required")

        if not self.stage_name:
            raise ValueError("stage_name is required")

        if self.default_order <= 0:
            raise ValueError("default_order must be positive")

        if self.default_duration_minutes is not None and self.default_duration_minutes <= 0:
            raise ValueError("default_duration_minutes must be positive")


@dataclass(slots=True)
class WorkflowTemplate:
    """Default order/product workflow template."""

    workflow_template_id: str
    template_name: str
    template_type: str
    version: str
    stages: tuple[WorkflowStageTemplate, ...]
    applies_to_product_id: str | None = None
    applies_to_service_id: str | None = None
    applies_to_order_type: str | None = None
    status: str = "draft"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.workflow_template_id:
            raise ValueError("workflow_template_id is required")

        if not self.template_name:
            raise ValueError("template_name is required")

        if not self.template_type:
            raise ValueError("template_type is required")

        if not self.version:
            raise ValueError("version is required")

        if not self.stages:
            raise ValueError("stages are required")

        self.stages = tuple(sorted(self.stages, key=lambda stage: stage.default_order))


@dataclass(slots=True)
class WorkflowStage:
    """Actual workflow stage for an order/order line."""

    workflow_stage_id: str
    order_id: str
    stage_code: str
    stage_name: str
    stage_order: int
    order_line_id: str | None = None
    status: str = "not_started"
    assigned_to: str | None = None
    contractor_ref: str | None = None
    subcontractor_ref: str | None = None
    planned_start_at: datetime | None = None
    planned_finish_at: datetime | None = None
    actual_start_at: datetime | None = None
    actual_finish_at: datetime | None = None
    deadline_at: datetime | None = None
    source_template_id: str | None = None
    manual_override_reason: str | None = None
    is_manual_stage: bool = False
    is_skipped: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.workflow_stage_id:
            raise ValueError("workflow_stage_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.stage_code:
            raise ValueError("stage_code is required")

        if not self.stage_name:
            raise ValueError("stage_name is required")

        if self.stage_order <= 0:
            raise ValueError("stage_order must be positive")

        ensure_in(self.status, WORKFLOW_STATUSES, "status")

        if self.is_manual_stage and not self.manual_override_reason:
            raise ValueError("manual_override_reason is required for manual stage")

    def is_late(self, now: datetime | None = None) -> bool:
        """Return whether stage is late."""

        if self.deadline_at is None:
            return False

        if self.status in {"completed", "cancelled"}:
            return False

        checked_at = now or utc_now()
        return checked_at > self.deadline_at


@dataclass(slots=True)
class ContractorReference:
    """Flexible contractor/subcontractor reference.

    This does not create a full supplier/contractor module.
    """

    contractor_reference_id: str
    contractor_type: str
    display_name: str
    client_account_id: str | None = None
    external_reference_id: str | None = None
    source_system: str = "manual"
    resolution_status: str = "display_only"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.contractor_reference_id:
            raise ValueError("contractor_reference_id is required")

        if not self.contractor_type:
            raise ValueError("contractor_type is required")

        if not self.display_name:
            raise ValueError("display_name is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        ensure_in(
            self.resolution_status,
            CONTRACTOR_RESOLUTION_STATUSES,
            "resolution_status",
        )

        if (
            self.resolution_status == "client_account_reference_confirmed"
            and not self.client_account_id
        ):
            raise ValueError("client_account_id is required when contractor reference is confirmed")


@dataclass(slots=True)
class DeadlineControlRecord:
    """Deadline control record for operational monitoring."""

    deadline_control_id: str
    target_entity_type: str
    target_entity_id: str
    deadline_type: str
    deadline_at: datetime
    warning_before_minutes: int | None = None
    status: str = "active"
    last_checked_at: datetime | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.deadline_control_id:
            raise ValueError("deadline_control_id is required")

        if not self.target_entity_type:
            raise ValueError("target_entity_type is required")

        if not self.target_entity_id:
            raise ValueError("target_entity_id is required")

        ensure_in(self.deadline_type, DEADLINE_TYPES, "deadline_type")
        ensure_in(self.status, DEADLINE_STATUSES, "status")

        if self.warning_before_minutes is not None and self.warning_before_minutes < 0:
            raise ValueError("warning_before_minutes must not be negative")
