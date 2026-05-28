from compliance_security_dashboard.validation.finding_validator import (
    validate_finding,
    validate_required_fields,
)


def test_validate_required_fields_accepts_complete_finding():
    finding = {
        "finding_id": "TEST-001",
        "title": "Sample",
        "resource_type": "user",
        "resource_name": "admin@example.invalid",
        "severity": "High",
        "category": "identity",
        "risk_score": 80,
        "recommendation": "Enable MFA.",
    }
    assert validate_required_fields(finding)


def test_validate_finding_reports_missing_required_field():
    issues = validate_finding({"finding_id": "TEST-001"})

    issue_fields = {issue.field for issue in issues}

    assert "title" in issue_fields
    assert "resource_type" in issue_fields


def test_validate_finding_reports_invalid_severity():
    issues = validate_finding(
        {
            "finding_id": "TEST-001",
            "title": "Sample",
            "resource_type": "user",
            "resource_name": "admin",
            "category": "identity",
            "severity": "urgent",
            "risk_score": 80,
            "recommendation": "Fix it.",
        }
    )

    assert any(issue.field == "severity" for issue in issues)


def test_validate_finding_reports_invalid_status():
    issues = validate_finding(
        {
            "finding_id": "TEST-001",
            "title": "Sample",
            "resource_type": "user",
            "resource_name": "admin",
            "category": "identity",
            "severity": "High",
            "status": "waiting",
            "risk_score": 80,
            "recommendation": "Fix it.",
        }
    )

    assert any(issue.field == "status" for issue in issues)


def test_validate_finding_reports_risk_score_bounds():
    issues = validate_finding(
        {
            "finding_id": "TEST-001",
            "title": "Sample",
            "resource_type": "user",
            "resource_name": "admin",
            "category": "identity",
            "severity": "High",
            "risk_score": 101,
            "recommendation": "Fix it.",
        }
    )

    assert any(issue.field == "risk_score" for issue in issues)


def test_validate_finding_reports_malformed_due_date():
    issues = validate_finding(
        {
            "finding_id": "TEST-001",
            "title": "Sample",
            "resource_type": "user",
            "resource_name": "admin",
            "category": "identity",
            "severity": "High",
            "risk_score": 80,
            "recommendation": "Fix it.",
            "due_date": "not-a-date",
        }
    )

    assert any(issue.field == "due_date" for issue in issues)
