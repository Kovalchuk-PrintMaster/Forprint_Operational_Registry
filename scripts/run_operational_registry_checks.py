"""Run local checks for ForPrint Operational Registry."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app"

if str(APP_PATH) not in sys.path:
    sys.path.insert(0, str(APP_PATH))

from forprint_operational_registry.services.registry_checks import (  # noqa: E402
    validate_blocker_config,
    validate_checkpoint_a_files,
    validate_checkpoint_b_files,
    validate_foreign_import_boundary,
    validate_handoff_fixtures,
    validate_macro_pack_files,
    validate_manifest,
    validate_no_production_api,
    validate_placeholder_contracts,
    validate_projection_fixtures,
    validate_required_docs,
    validate_status_config,
    validate_v02_boundary_files,
)

console = Console()


@dataclass
class CheckStep:
    """Single check-report step."""

    name: str
    expected_result: str
    ok: bool
    duration_seconds: float
    details: str


def format_duration(duration_seconds: float) -> str:
    """Format duration for console and reports."""

    return f"{duration_seconds:.2f}s"


def run_command(
    name: str,
    expected_result: str,
    command: list[str],
) -> CheckStep:
    """Run external command and return check step result."""

    started_at = time.perf_counter()

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    duration_seconds = time.perf_counter() - started_at

    details = result.stdout.strip()
    if result.stderr.strip():
        details = f"{details}\n{result.stderr.strip()}".strip()

    ok = result.returncode == 0

    return CheckStep(
        name=name,
        expected_result=expected_result,
        ok=ok,
        duration_seconds=duration_seconds,
        details=details or "OK",
    )


def run_internal_check(
    name: str,
    expected_result: str,
    errors: list[str],
) -> CheckStep:
    """Convert internal validation errors to a check step."""

    started_at = time.perf_counter()
    duration_seconds = time.perf_counter() - started_at

    return CheckStep(
        name=name,
        expected_result=expected_result,
        ok=not errors,
        duration_seconds=duration_seconds,
        details="OK" if not errors else "\n".join(errors),
    )


def build_check_report(run_external: bool = True) -> dict[str, object]:
    """Build full check report."""

    steps: list[CheckStep] = []

    if run_external:
        steps.append(
            run_command(
                name="Ruff lint",
                expected_result="Немає lint-помилок у app/tests/scripts",
                command=[
                    sys.executable,
                    "-m",
                    "ruff",
                    "check",
                    "app",
                    "tests",
                    "scripts",
                ],
            )
        )

        steps.append(
            run_command(
                name="Pytest",
                expected_result="Усі тести проходять",
                command=[
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                ],
            )
        )

    steps.append(
        run_internal_check(
            name="Module manifest boundary",
            expected_result="Manifest відповідає ролі operational truth registry",
            errors=validate_manifest(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Required architecture docs",
            expected_result="Усі boundary-документи існують",
            errors=validate_required_docs(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Status config",
            expected_result="Статуси відповідають Blueprint v0.1",
            errors=validate_status_config(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Command/query service boundary",
            expected_result="DTO/repository/service файли v0.2 існують",
            errors=validate_v02_boundary_files(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="No production API",
            expected_result="Production API не додано у v0.2",
            errors=validate_no_production_api(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Checkpoint A files",
            expected_result="Envelope/reference/placeholder contract files exist",
            errors=validate_checkpoint_a_files(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Placeholder contracts",
            expected_result="Placeholder contracts are non-canonical local fixtures",
            errors=validate_placeholder_contracts(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Foreign import boundary",
            expected_result="No real foreign runtime imports or integration adapters",
            errors=validate_foreign_import_boundary(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Checkpoint B files",
            expected_result="Lifecycle/blocker files exist",
            errors=validate_checkpoint_b_files(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Macro pack files",
            expected_result="Projection/readiness/status export files exist",
            errors=validate_macro_pack_files(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Handoff fixtures",
            expected_result="Offline handoff fixtures are valid examples",
            errors=validate_handoff_fixtures(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Projection fixtures",
            expected_result="Projection example fixtures are valid",
            errors=validate_projection_fixtures(PROJECT_ROOT),
        )
    )

    steps.append(
        run_internal_check(
            name="Operational blocker config",
            expected_result="Operational blocker config is valid",
            errors=validate_blocker_config(PROJECT_ROOT),
        )
    )

    return {
        "module_id": "forprint_operational_registry",
        "module_name": "ForPrint Operational Registry",
        "created_at": datetime.now(UTC).isoformat(),
        "ok": all(step.ok for step in steps),
        "steps": [asdict(step) for step in steps],
    }


def write_reports(report: dict[str, object]) -> tuple[Path, Path]:
    """Write JSON and Markdown reports."""

    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    json_path = reports_dir / "operational_registry_check_report.json"
    md_path = reports_dir / "operational_registry_check_report.md"

    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    overall_status = "OK" if report["ok"] else "FAILED"

    lines = [
        "# ForPrint Operational Registry Check Report",
        "",
        f"- Module: `{report['module_id']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Overall status: `{overall_status}`",
        "",
        "## Steps",
        "",
        "| Перевірка | Очікуваний результат | Статус | Час |",
        "|---|---|---|---|",
    ]

    for step in report["steps"]:
        status = "OK" if step["ok"] else "FAILED"
        duration = format_duration(step["duration_seconds"])
        lines.append(f"| {step['name']} | {step['expected_result']} | {status} | {duration} |")

    lines.extend(
        [
            "",
            "## Details",
            "",
        ]
    )

    for step in report["steps"]:
        status = "OK" if step["ok"] else "FAILED"
        lines.extend(
            [
                f"### {step['name']}",
                "",
                f"Status: `{status}`",
                "",
                "```text",
                step["details"],
                "```",
                "",
            ]
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path


def print_step_progress(step: CheckStep) -> None:
    """Print short progress line after each check."""

    status = "[green]OK[/green]" if step.ok else "[red]FAILED[/red]"
    duration = format_duration(step.duration_seconds)
    console.print(f"  - {step.name}: {status} ({duration})")


def print_report_table(report: dict[str, object]) -> None:
    """Print rich console table."""

    table = Table(title="ForPrint Operational Registry — check report")

    table.add_column("Перевірка", style="cyan", no_wrap=True)
    table.add_column("Очікуваний результат")
    table.add_column("Статус", justify="center")
    table.add_column("Час", justify="right")

    for step in report["steps"]:
        status = "[green]OK[/green]" if step["ok"] else "[red]FAILED[/red]"
        duration = format_duration(step["duration_seconds"])

        table.add_row(
            step["name"],
            step["expected_result"],
            status,
            duration,
        )

    console.print()
    console.print(table)


def print_failed_details(report: dict[str, object]) -> None:
    """Print details for failed checks."""

    failed_steps = [step for step in report["steps"] if not step["ok"]]

    if not failed_steps:
        return

    for step in failed_steps:
        console.print()
        console.print(
            Panel(
                step["details"],
                title=f"[red]{step['name']} details[/red]",
                border_style="red",
            )
        )


def main() -> int:
    """CLI entrypoint."""

    console.print("🔎 Running ForPrint Operational Registry checks...")

    report = build_check_report(run_external=True)

    for step_data in report["steps"]:
        step = CheckStep(**step_data)
        print_step_progress(step)

    json_path, md_path = write_reports(report)

    print_report_table(report)
    print_failed_details(report)

    console.print(f"📄 JSON report: {json_path}")
    console.print(f"📄 Markdown report: {md_path}")

    if report["ok"]:
        console.print("[green]✅ Check report completed successfully.[/green]")
        return 0

    console.print("[red]❌ Check report failed.[/red]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
