"""Demo services for order/workflow/projection foundation.

These helpers operate on in-memory demo records only.
No runtime integrations are performed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from uuid import uuid4

from forprint_operational_registry.models.data_foundation import (
    DataProjection,
)
from forprint_operational_registry.models.order_workflow import (
    AlertEvent,
    AlertRule,
    MaterialRequirement,
    OperationalOrder,
    OperationalOrderLine,
    PaymentProjection,
    WorkflowStage,
    WorkflowStageTemplate,
    WorkflowTemplate,
)


class OrderWorkflowDemoService:
    """Small helper for demo order behavior."""

    def __init__(self) -> None:
        self.orders: dict[str, OperationalOrder] = {}
        self.lines: dict[str, OperationalOrderLine] = {}

    def create_order(self, order: OperationalOrder) -> OperationalOrder:
        """Create demo order."""

        self.orders[order.order_id] = order
        return order

    def add_order_line(self, line: OperationalOrderLine) -> OperationalOrderLine:
        """Add demo order line."""

        if line.order_id not in self.orders:
            raise KeyError(f"Order not found: {line.order_id}")

        self.lines[line.order_line_id] = line
        return line

    def change_order_status(self, order_id: str, status: str) -> OperationalOrder:
        """Change demo order status."""

        order = self.orders[order_id]
        order.status = status
        order.updated_at = datetime.now(tz=order.updated_at.tzinfo)
        return order

    def summarize_order_status(self) -> dict[str, int]:
        """Summarize orders by status."""

        return dict(Counter(order.status for order in self.orders.values()))


class WorkflowStageService:
    """Demo workflow stage helper."""

    def create_stages_from_template(
        self,
        order_id: str,
        template: WorkflowTemplate,
    ) -> list[WorkflowStage]:
        """Create ordered stages from workflow template."""

        return [
            WorkflowStage(
                workflow_stage_id=f"stage_{order_id}_{stage.stage_code}",
                order_id=order_id,
                stage_code=stage.stage_code,
                stage_name=stage.stage_name,
                stage_order=stage.default_order,
                source_template_id=template.workflow_template_id,
            )
            for stage in template.stages
        ]

    def add_manual_stage(
        self,
        order_id: str,
        stage_code: str,
        stage_name: str,
        stage_order: int,
        reason: str,
    ) -> WorkflowStage:
        """Add manual workflow stage."""

        return WorkflowStage(
            workflow_stage_id=f"stage_{uuid4().hex}",
            order_id=order_id,
            stage_code=stage_code,
            stage_name=stage_name,
            stage_order=stage_order,
            is_manual_stage=True,
            manual_override_reason=reason,
        )

    @staticmethod
    def mark_in_progress(stage: WorkflowStage) -> WorkflowStage:
        """Mark stage in progress."""

        stage.status = "in_progress"
        stage.actual_start_at = datetime.now(tz=stage.created_at.tzinfo)
        return stage

    @staticmethod
    def mark_completed(stage: WorkflowStage) -> WorkflowStage:
        """Mark stage completed."""

        stage.status = "completed"
        stage.actual_finish_at = datetime.now(tz=stage.created_at.tzinfo)
        return stage

    @staticmethod
    def detect_late_stage(stage: WorkflowStage, now: datetime | None = None) -> bool:
        """Detect late stage."""

        return stage.is_late(now=now)

    @staticmethod
    def summarize_stages_by_order(stages: list[WorkflowStage]) -> dict[str, int]:
        """Summarize workflow stages by status."""

        return dict(Counter(stage.status for stage in stages))


class MaterialRequirementService:
    """Demo material requirement helper."""

    def __init__(self) -> None:
        self.requirements: list[MaterialRequirement] = []

    def add_material_requirement(
        self,
        requirement: MaterialRequirement,
    ) -> MaterialRequirement:
        """Add material requirement."""

        self.requirements.append(requirement)
        return requirement

    def list_requirements_by_order(self, order_id: str) -> list[MaterialRequirement]:
        """List requirements by order."""

        return [
            requirement for requirement in self.requirements if requirement.order_id == order_id
        ]

    def list_requirements_by_period(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> list[MaterialRequirement]:
        """List requirements by required_by period."""

        return [
            requirement
            for requirement in self.requirements
            if requirement.required_by is not None
            and period_start <= requirement.required_by <= period_end
        ]

    def detect_unresolved_requirements(self) -> list[MaterialRequirement]:
        """Return unresolved material requirements."""

        return [requirement for requirement in self.requirements if requirement.is_unresolved]


class PaymentProjectionService:
    """Demo payment projection helper."""

    def __init__(self) -> None:
        self.projections: list[PaymentProjection] = []

    def create_payment_projection(
        self,
        projection: PaymentProjection,
    ) -> PaymentProjection:
        """Create payment projection."""

        self.projections.append(projection)
        return projection

    @staticmethod
    def calculate_unpaid_amount(projection: PaymentProjection) -> float:
        """Calculate unpaid amount."""

        return projection.unpaid_amount

    @staticmethod
    def mark_overdue(projection: PaymentProjection) -> PaymentProjection:
        """Mark projection overdue."""

        projection.payment_status = "overdue"
        return projection

    def summarize_debt_by_client(self) -> dict[str, float]:
        """Summarize unpaid amount by ClientAccount."""

        result: dict[str, float] = defaultdict(float)
        for projection in self.projections:
            result[projection.client_account_id] += projection.unpaid_amount

        return {client_id: round(amount, 2) for client_id, amount in result.items()}


class AlertEvaluationService:
    """Demo alert evaluation helper."""

    def create_late_stage_alert(
        self,
        stage: WorkflowStage,
        rule: AlertRule,
        now: datetime | None = None,
    ) -> AlertEvent | None:
        """Create alert event for late workflow stage."""

        if not rule.is_active or not stage.is_late(now=now):
            return None

        return AlertEvent(
            alert_event_id=f"alert_{uuid4().hex}",
            alert_rule_id=rule.alert_rule_id,
            target_entity_type="workflow_stage",
            target_entity_id=stage.workflow_stage_id,
            severity=rule.severity,
            status="open",
            message=f"Workflow stage is late: {stage.stage_name}",
            notification_status="not_sent",
        )

    def create_overdue_payment_alert(
        self,
        projection: PaymentProjection,
        rule: AlertRule,
    ) -> AlertEvent | None:
        """Create alert event for overdue payment projection."""

        if not rule.is_active or projection.payment_status != "overdue":
            return None

        return AlertEvent(
            alert_event_id=f"alert_{uuid4().hex}",
            alert_rule_id=rule.alert_rule_id,
            target_entity_type="payment_projection",
            target_entity_id=projection.payment_projection_id,
            severity=rule.severity,
            status="open",
            message=f"Payment is overdue for order {projection.order_id}",
            notification_status="not_sent",
        )

    def create_unresolved_material_alert(
        self,
        requirement: MaterialRequirement,
        rule: AlertRule,
    ) -> AlertEvent | None:
        """Create alert event for unresolved material requirement."""

        if not rule.is_active or not requirement.is_unresolved:
            return None

        return AlertEvent(
            alert_event_id=f"alert_{uuid4().hex}",
            alert_rule_id=rule.alert_rule_id,
            target_entity_type="material_requirement",
            target_entity_id=requirement.material_requirement_id,
            severity=rule.severity,
            status="open",
            message=f"Material requirement is unresolved: {requirement.material_display_name}",
            notification_status="not_sent",
        )


class OperationalReportService:
    """Demo operational report helper."""

    def produce_client_order_history(
        self,
        orders: list[OperationalOrder],
    ) -> DataProjection:
        """Produce demo client order history projection."""

        rows = [
            {
                "client_account_id": order.client_account_id,
                "order_id": order.order_id,
                "status": order.status,
                "currency": order.currency,
                "total_amount_planned": order.total_amount_planned,
            }
            for order in orders
        ]

        return DataProjection(
            projection_id="projection_client_order_history_demo",
            projection_type="client_order_history",
            dimensions=("client_account_id", "order_id", "status"),
            metrics=("total_amount_planned",),
            rows=tuple(rows),
        )

    def produce_payment_debt_summary(
        self,
        projections: list[PaymentProjection],
    ) -> DataProjection:
        """Produce demo payment/debt summary."""

        debt_by_client: dict[str, float] = defaultdict(float)
        for projection in projections:
            debt_by_client[projection.client_account_id] += projection.unpaid_amount

        return DataProjection(
            projection_id="projection_payment_debt_summary_demo",
            projection_type="payment_debt_summary",
            dimensions=("client_account_id",),
            metrics=("unpaid_amount",),
            rows=tuple(
                {
                    "client_account_id": client_account_id,
                    "unpaid_amount": round(amount, 2),
                }
                for client_account_id, amount in debt_by_client.items()
            ),
        )

    def produce_workflow_status_summary(
        self,
        stages: list[WorkflowStage],
    ) -> DataProjection:
        """Produce demo workflow status summary."""

        counts = Counter(stage.status for stage in stages)

        return DataProjection(
            projection_id="projection_workflow_status_summary_demo",
            projection_type="workflow_stage_status",
            dimensions=("status",),
            metrics=("stage_count",),
            rows=tuple(
                {"status": status, "stage_count": count} for status, count in counts.items()
            ),
        )

    def produce_alert_summary(self, alerts: list[AlertEvent]) -> DataProjection:
        """Produce demo alert summary."""

        counts = Counter(alert.status for alert in alerts)

        return DataProjection(
            projection_id="projection_alert_summary_demo",
            projection_type="alert_summary",
            dimensions=("status",),
            metrics=("alert_count",),
            rows=tuple(
                {"status": status, "alert_count": count} for status, count in counts.items()
            ),
        )


def demo_workflow_template() -> WorkflowTemplate:
    """Return demo workflow template."""

    return WorkflowTemplate(
        workflow_template_id="wf_template_demo_001",
        template_name="Demo order workflow",
        template_type="order",
        version="0.1",
        stages=(
            WorkflowStageTemplate(
                stage_code="prepress",
                stage_name="Prepress",
                default_order=1,
                default_duration_minutes=120,
                responsible_role="prepress_operator",
            ),
            WorkflowStageTemplate(
                stage_code="production",
                stage_name="Production",
                default_order=2,
                default_duration_minutes=240,
                responsible_role="production_operator",
            ),
            WorkflowStageTemplate(
                stage_code="quality_check",
                stage_name="Quality Check",
                default_order=3,
                default_duration_minutes=60,
                responsible_role="operator",
            ),
        ),
    )
