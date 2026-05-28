from compliance_security_dashboard.validation.finding_validator import (
    validate_required_fields,
)


def test_validate_required_fields_accepts_complete_finding():
    finding = {
        "finding_id": "TEST-001",
        "source_system": "saas",
        "title": "Sample",
        "severity": "high",
        "category": "identity",
        "owner": "Security",
        "status": "open",
    }
    assert validate_required_fields(finding)
