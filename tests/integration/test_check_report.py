from scripts.run_operational_registry_checks import build_check_report


def test_check_report_internal_validations_pass() -> None:
    report = build_check_report(run_external=False)

    assert report["ok"] is True
