from forprint_operational_registry.models.task import OperationalTask


def test_operational_task_can_be_created() -> None:
    task = OperationalTask(
        task_id="task_001",
        order_id="order_001",
        task_type="prepress_review",
        assigned_to_ref="operator_001",
    )

    assert task.task_id == "task_001"
    assert task.order_id == "order_001"
    assert task.task_status == "new"
