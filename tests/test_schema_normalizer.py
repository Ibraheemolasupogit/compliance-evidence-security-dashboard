from compliance_security_dashboard.normalization.schema_normalizer import (
    normalize_finding,
)


def test_normalize_finding_returns_unified_finding():
    raw = {
        "finding_id": "SAAS-001",
        "source_system": "saas",
        "title": "MFA not enforced for admin users",
        "severity": "high",
        "category": "identity",
        "owner": "SaaS Platform Team",
        "status": "open",
        "observed_at": "2026-05-01",
        "evidence": "Offline sample finding",
    }

    normalized = normalize_finding(raw, source_name="saas")

    assert normalized.finding_id == "SAAS-001"
    assert normalized.source_system == "saas"
    assert normalized.source_repo == "saas-security-posture-monitoring"
    assert normalized.risk_score == 75
    assert normalized.control_mapping == "CTRL-IAM-001"
    assert normalized.due_date == "2026-05-15"
    assert normalized.evidence_completeness_score == 100
