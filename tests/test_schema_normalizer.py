from compliance_security_dashboard.normalization.field_mapper import (
    map_severity,
    map_status,
)
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
    assert normalized.severity == "High"
    assert normalized.status == "Open"
    assert normalized.risk_score == 80
    assert normalized.control_mapping == "CTRL-IAM-001"
    assert normalized.due_date == "2026-05-15"
    assert normalized.evidence_completeness_score == 100


def test_map_severity_standardizes_variants():
    assert map_severity("CRITICAL") == "Critical"
    assert map_severity("med") == "Medium"
    assert map_severity("informational") == "Info"


def test_map_status_standardizes_variants():
    assert map_status("in_progress") == "In Progress"
    assert map_status("accepted") == "Risk Accepted"
    assert map_status("closed") == "Remediated"
