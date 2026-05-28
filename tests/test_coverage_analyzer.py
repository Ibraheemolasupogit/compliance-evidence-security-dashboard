from compliance_security_dashboard.compliance.coverage_analyzer import (
    build_control_coverage_summary,
    build_control_mapping_summary,
)


def test_build_control_mapping_summary_dataframe():
    summary = build_control_mapping_summary(
        [
            {
                "finding_id": "TEST-001",
                "cis_control": "CIS 6",
                "nist_category": "PR.AC",
                "iso_domain": "Access Control",
                "category": "identity",
                "severity": "High",
                "risk_score": 80,
                "status": "Open",
                "evidence_completeness_score": 80,
            },
            {
                "finding_id": "TEST-002",
                "cis_control": "CIS 6",
                "nist_category": "PR.AC",
                "iso_domain": "Access Control",
                "category": "identity",
                "severity": "High",
                "risk_score": 90,
                "status": "Remediated",
                "evidence_completeness_score": 60,
            },
        ]
    )

    assert summary.loc[0, "finding_count"] == 2
    assert summary.loc[0, "average_risk_score"] == 85
    assert summary.loc[0, "max_risk_score"] == 90
    assert summary.loc[0, "open_findings"] == 1
    assert summary.loc[0, "average_evidence_completeness_score"] == 70


def test_build_control_coverage_summary_metrics():
    summary = build_control_coverage_summary(
        [
            {
                "finding_id": "TEST-001",
                "control_mapping": "CTRL-IAM-001",
                "cis_control": "CIS 6",
                "nist_category": "PR.AC",
                "iso_domain": "Access Control",
                "severity": "High",
                "evidence_completeness_score": 80,
            },
            {
                "finding_id": "TEST-002",
                "control_mapping": "",
                "cis_control": "",
                "nist_category": "",
                "iso_domain": "",
                "severity": "Low",
                "evidence_completeness_score": 40,
            },
        ]
    )

    assert summary["total_findings"] == 2
    assert summary["mapped_findings"] == 1
    assert summary["unmapped_findings"] == 1
    assert summary["mapping_coverage_percent"] == 50
    assert summary["controls_with_findings"] == 1
    assert summary["high_or_critical_control_findings"] == 1
