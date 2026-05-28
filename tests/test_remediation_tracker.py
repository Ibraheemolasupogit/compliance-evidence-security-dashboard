from datetime import date

from compliance_security_dashboard.remediation.remediation_tracker import (
    apply_sla_statuses,
    build_remediation_owner_summary,
    build_remediation_summary,
    build_remediation_tracker,
    filter_due_soon_findings,
    filter_overdue_findings,
)


def sample_findings():
    return [
        {
            "finding_id": "TEST-001",
            "title": "Overdue finding",
            "severity": "High",
            "risk_score": 80,
            "source_repo": "repo-a",
            "source_system": "saas",
            "category": "identity",
            "cis_control": "CIS 6",
            "nist_category": "PR.AC",
            "iso_domain": "Access Control",
            "remediation_owner": "Owner A",
            "status": "Open",
            "due_date": "2026-05-20",
            "recommendation": "Fix it.",
            "evidence_completeness_score": 80,
        },
        {
            "finding_id": "TEST-002",
            "title": "Due soon finding",
            "severity": "Medium",
            "risk_score": 55,
            "source_repo": "repo-b",
            "source_system": "snowflake",
            "category": "access_governance",
            "cis_control": "CIS 5",
            "nist_category": "PR.AC",
            "iso_domain": "Access Control",
            "remediation_owner": "Owner A",
            "status": "In Progress",
            "due_date": "2026-06-02",
            "recommendation": "Fix it.",
            "evidence_completeness_score": 60,
        },
        {
            "finding_id": "TEST-003",
            "title": "Closed finding",
            "severity": "Low",
            "risk_score": 25,
            "source_repo": "repo-c",
            "source_system": "iam",
            "category": "privileged_access",
            "cis_control": "CIS 6",
            "nist_category": "PR.AC",
            "iso_domain": "Access Control",
            "remediation_owner": "Owner B",
            "status": "Remediated",
            "due_date": "2026-05-01",
            "recommendation": "Fixed.",
            "evidence_completeness_score": 100,
        },
    ]


def test_build_remediation_tracker_dataframe():
    findings = apply_sla_statuses(sample_findings(), today=date(2026, 5, 28))
    tracker = build_remediation_tracker(findings)

    assert len(tracker) == 3
    assert tracker.loc[0, "sla_status"] == "Overdue"
    assert "recommendation" in tracker.columns


def test_build_remediation_summary_dataframe():
    findings = apply_sla_statuses(sample_findings(), today=date(2026, 5, 28))
    summary = build_remediation_summary(findings)

    assert {"Owner A", "Owner B"} == set(summary["remediation_owner"])
    assert summary["finding_count"].sum() == 3


def test_build_remediation_owner_summary_dataframe():
    findings = apply_sla_statuses(sample_findings(), today=date(2026, 5, 28))
    summary = build_remediation_owner_summary(findings)
    owner_a = summary[summary["remediation_owner"] == "Owner A"].iloc[0]

    assert owner_a["total_findings"] == 2
    assert owner_a["open_findings"] == 2
    assert owner_a["overdue_findings"] == 1
    assert owner_a["due_soon_findings"] == 1
    assert owner_a["high_or_critical_findings"] == 1


def test_filter_overdue_findings():
    findings = apply_sla_statuses(sample_findings(), today=date(2026, 5, 28))
    overdue = filter_overdue_findings(findings)

    assert list(overdue["finding_id"]) == ["TEST-001"]


def test_filter_due_soon_findings():
    findings = apply_sla_statuses(sample_findings(), today=date(2026, 5, 28))
    due_soon = filter_due_soon_findings(findings)

    assert list(due_soon["finding_id"]) == ["TEST-002"]
