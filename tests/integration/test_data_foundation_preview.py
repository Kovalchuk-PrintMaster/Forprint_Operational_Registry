from scripts.data_foundation_preview import render_data_foundation_preview


def test_data_foundation_preview_renders_key_sections() -> None:
    output = render_data_foundation_preview()

    assert "ForPrint Operational Registry — Data Foundation Preview" in output
    assert "MASTER DATA BASE RECORD" in output
    assert "OPERATIONAL FACT RECORD" in output
    assert "EVENT RECORD" in output
    assert "EXTERNAL REFERENCES" in output
    assert "REPORT DEFINITION" in output
    assert "DATA PROJECTION" in output
    assert "EXAMPLE REPORT QUESTIONS" in output
