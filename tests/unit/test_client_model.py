import pytest
from forprint_operational_registry.models.client import ClientRecord


def test_client_record_can_be_created() -> None:
    client = ClientRecord(
        client_id="client_001",
        display_name="Test Client",
        contact_refs=["telegram:user:123"],
        source_refs={"crm": "crm_client_001"},
    )

    assert client.client_id == "client_001"
    assert client.display_name == "Test Client"


def test_client_record_does_not_become_crm_profile() -> None:
    with pytest.raises(ValueError, match="must not become CRM profile"):
        ClientRecord(
            client_id="client_001",
            display_name="Test Client",
            metadata={"sales_pipeline": "lead"},
        )
