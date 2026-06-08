"""Render safe demo ClientAccount card in terminal."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLE = PROJECT_ROOT / "examples/client_cards/demo_organization_client.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping: {path}")
    return data


def render_table(title: str, headers: list[str], rows: list[list[Any]]) -> str:
    """Render simple Unicode table."""

    string_rows = [[str(cell) if cell is not None else "" for cell in row] for row in rows]
    string_headers = [str(header) for header in headers]
    widths = [
        max(len(string_headers[index]), *(len(row[index]) for row in string_rows))
        for index in range(len(string_headers))
    ]

    def row_line(values: list[str]) -> str:
        return (
            "│ "
            + " │ ".join(value.ljust(widths[index]) for index, value in enumerate(values))
            + " │"
        )

    top = "┌" + "┬".join("─" * (width + 2) for width in widths) + "┐"
    mid = "├" + "┼".join("─" * (width + 2) for width in widths) + "┤"
    bottom = "└" + "┴".join("─" * (width + 2) for width in widths) + "┘"

    lines = [title, top, row_line(string_headers), mid]
    lines.extend(row_line(row) for row in string_rows)
    lines.append(bottom)
    return "\n".join(lines)


def key_value_table(title: str, payload: dict[str, Any], keys: list[str]) -> str:
    """Render selected dict keys as key/value table."""

    rows = [[key, payload.get(key, "")] for key in keys]
    return render_table(title, ["Field", "Value"], rows)


def render_client_card_preview(data: dict[str, Any]) -> str:
    """Render full demo client card preview."""

    account = data["client_account"]

    sections = [
        "ForPrint Operational Registry — Client Card Preview",
        "",
        key_value_table(
            "CLIENT ACCOUNT",
            account,
            [
                "client_account_id",
                "account_type",
                "display_name",
                "common_name",
                "legal_name",
                "status",
                "legacy_raw_name",
            ],
        ),
        "",
        render_table(
            "CONTACT METHODS",
            ["method_id", "type", "kind", "normalized", "primary"],
            [
                [
                    method.get("contact_method_id"),
                    method.get("method_type"),
                    method.get("kind"),
                    method.get("normalized_value"),
                    "yes" if method.get("is_primary") else "no",
                ]
                for method in data.get("contact_methods", [])
            ],
        ),
        "",
        render_table(
            "CONTACT PERSONS",
            ["person_id", "full_name", "preferred", "position", "status"],
            [
                [
                    person.get("contact_person_id"),
                    person.get("full_name"),
                    person.get("preferred_name"),
                    person.get("position"),
                    person.get("status"),
                ]
                for person in data.get("contact_persons", [])
            ],
        ),
        "",
        render_table(
            "ACCOUNT-CONTACT LINKS",
            ["link_id", "account_id", "person_id", "method_id", "role", "primary"],
            [
                [
                    link.get("account_contact_link_id"),
                    link.get("client_account_id"),
                    link.get("contact_person_id"),
                    link.get("contact_method_id"),
                    link.get("role"),
                    "yes" if link.get("is_primary") else "no",
                ]
                for link in data.get("account_contact_links", [])
            ],
        ),
        "",
        render_table(
            "ADDRESSES",
            ["address_id", "type", "raw", "service", "primary"],
            [
                [
                    address.get("client_address_id"),
                    address.get("address_type"),
                    address.get("raw_presentation"),
                    address.get("delivery_service"),
                    "yes" if address.get("is_primary") else "no",
                ]
                for address in data.get("addresses", [])
            ],
        ),
        "",
        render_table(
            "LEGAL PROFILE",
            ["profile_id", "type", "legal_name", "edrpou", "tax_scheme"],
            [
                [
                    profile.get("legal_entity_profile_id"),
                    profile.get("legal_entity_type"),
                    profile.get("legal_name"),
                    profile.get("edrpou"),
                    profile.get("tax_scheme"),
                ]
                for profile in data.get("legal_profiles", [])
            ],
        ),
        "",
        render_table(
            "EXTERNAL ACCOUNTING REFERENCES",
            ["ref_id", "entity", "source", "code", "external_name"],
            [
                [
                    reference.get("external_reference_id"),
                    reference.get("entity_type"),
                    reference.get("source_system"),
                    reference.get("external_code"),
                    reference.get("external_name"),
                ]
                for reference in data.get("external_accounting_references", [])
            ],
        ),
        "",
        render_table(
            "CONTRACTS",
            ["contract_id", "name", "type", "settlement", "source"],
            [
                [
                    contract.get("client_contract_id"),
                    contract.get("contract_name"),
                    contract.get("contract_type"),
                    contract.get("settlement_mode"),
                    contract.get("source_system"),
                ]
                for contract in data.get("contracts", [])
            ],
        ),
        "",
        render_table(
            "NOTES / PREFERENCES",
            ["kind", "type", "value"],
            [["note", note.get("note_type"), note.get("content")] for note in data.get("notes", [])]
            + [
                ["preference", preference.get("preference_type"), preference.get("value")]
                for preference in data.get("preferences", [])
            ],
        ),
    ]

    return "\n".join(sections)


def main() -> int:
    """CLI entrypoint."""

    data = load_yaml(DEFAULT_EXAMPLE)
    print(render_client_card_preview(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
