import pytest
from forprint_operational_registry.models.event import OperationalEvent


def test_operational_event_can_be_created() -> None:
    event = OperationalEvent(
        event_id="evt_001",
        entity_type="order",
        entity_id="order_001",
        event_type="order_created",
        actor_ref="operator_001",
        source_module="forprint_operational_registry",
        payload={"status": "new"},
    )

    assert event.event_id == "evt_001"
    assert event.payload["status"] == "new"


def test_operational_event_payload_is_immutable() -> None:
    event = OperationalEvent(
        event_id="evt_001",
        entity_type="order",
        entity_id="order_001",
        event_type="order_created",
        actor_ref="operator_001",
        source_module="forprint_operational_registry",
        payload={"status": "new"},
    )

    with pytest.raises(TypeError):
        event.payload["status"] = "changed"
