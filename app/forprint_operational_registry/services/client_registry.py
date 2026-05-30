"""Client registry service for Operational Registry v0.2."""

from forprint_operational_registry.dto.commands import CreateClientCommand
from forprint_operational_registry.models.client import ClientRecord
from forprint_operational_registry.repositories.interfaces import ClientRepository


class ClientRegistryService:
    """Create/read canonical operational client identity."""

    def __init__(self, clients: ClientRepository) -> None:
        self._clients = clients

    def create_client(self, command: CreateClientCommand) -> ClientRecord:
        """Create operational client identity from command DTO."""

        client = ClientRecord(
            client_id=command.client_id,
            display_name=command.display_name,
            contact_refs=list(command.contact_refs),
            source_refs=command.source_refs,
            status=command.status,
            metadata=command.metadata,
        )
        self._clients.add(client)
        return client

    def get_client(self, client_id: str) -> ClientRecord | None:
        """Get client by id."""

        return self._clients.get(client_id)
