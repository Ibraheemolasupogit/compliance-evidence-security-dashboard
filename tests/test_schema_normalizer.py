from compliance_security_dashboard.normalization.schema_normalizer import (
    normalize_finding,
)


def test_normalize_finding_returns_copy():
    raw = {"finding_id": "TEST-001"}
    normalized = normalize_finding(raw)
    assert normalized == raw
    assert normalized is not raw
