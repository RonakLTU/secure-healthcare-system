from app.security.input_validation import sanitize_input


def test_sanitize_input():

    malicious = "<script>alert(1)</script>"

    cleaned = sanitize_input(malicious)

    assert "<" not in cleaned
    assert ">" not in cleaned