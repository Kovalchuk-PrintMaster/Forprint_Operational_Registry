from scripts.export_module_status import build_module_status, export_module_status


def test_module_status_export_runs() -> None:
    path = export_module_status()

    assert path.exists()


def test_module_status_includes_boundaries() -> None:
    status = build_module_status()

    assert status["module_id"] == "forprint_operational_registry"
    assert "operational_blockers" in status["implemented_layers"]
    assert "operational_projections" in status["implemented_layers"]
    assert "must_not_own" in status
    assert status["boundary_marker"]["no_real_integrations"] is True
    assert status["boundary_marker"]["no_foreign_runtime_data"] is True
