"""Operational status definitions for ForPrint Operational Registry v0.1."""

ORDER_STATUSES: tuple[str, ...] = (
    "new",
    "needs_review",
    "quote_pending",
    "quote_accepted",
    "payment_reference_pending",
    "payment_reference_confirmed",
    "in_prepress",
    "ready_for_production",
    "in_production",
    "ready_for_pickup",
    "completed",
    "cancelled",
    "blocked",
)

TASK_STATUSES: tuple[str, ...] = (
    "new",
    "assigned",
    "in_progress",
    "blocked",
    "completed",
    "cancelled",
)

FORBIDDEN_OPERATIONAL_STATUSES: tuple[str, ...] = ("paid",)

RECOMMENDED_SOURCE_CHANNELS: tuple[str, ...] = (
    "telegram_bot",
    "website",
    "mobile_app",
    "crm_manual",
    "gateway_import",
    "internal_module",
    "legacy_import",
)


def ensure_allowed_order_status(status: str) -> str:
    """Validate canonical order status for v0.1."""

    if status in FORBIDDEN_OPERATIONAL_STATUSES:
        raise ValueError(
            f"'{status}' is forbidden as Operational Registry payment truth. "
            "Use payment_reference_pending or payment_reference_confirmed instead."
        )

    if status not in ORDER_STATUSES:
        raise ValueError(f"Unknown order status: {status}")

    return status


def ensure_allowed_task_status(status: str) -> str:
    """Validate task status for v0.1."""

    if status not in TASK_STATUSES:
        raise ValueError(f"Unknown task status: {status}")

    return status
