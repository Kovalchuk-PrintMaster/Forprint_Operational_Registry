from scripts.dictionary_mapping_preview import render_dictionary_mapping_preview


def test_dictionary_mapping_preview_renders_key_sections() -> None:
    output = render_dictionary_mapping_preview()

    assert "DICTIONARY VERSION PIN" in output
    assert "MAPPED GROUPS" in output
    assert "CONFIRMED MAPPINGS" in output
    assert "UNRESOLVED VALUES" in output
    assert "DEPRECATED REFERENCES" in output
    assert "MANUAL REVIEW REQUIRED" in output
    assert "ALIGNMENT SUMMARY" in output
