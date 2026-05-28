from compliance_security_dashboard.scoring.evidence_scorer import (
    build_evidence_quality_summary,
    score_evidence_completeness,
    score_evidence_quality,
)


def test_score_evidence_quality_with_evidence():
    assert score_evidence_quality(True) == 100


def test_score_evidence_completeness():
    finding = {
        "evidence": "Sample",
        "resource_id": "",
        "recommendation": "Fix it.",
        "control_mapping": "CTRL-001",
        "remediation_owner": "Security",
    }

    assert score_evidence_completeness(finding) == 80


def test_build_evidence_quality_summary_dataframe():
    summary = build_evidence_quality_summary(
        [
            {
                "finding_id": "TEST-001",
                "source_repo": "repo-a",
                "category": "identity",
                "evidence_completeness_score": 80,
            },
            {
                "finding_id": "TEST-002",
                "source_repo": "repo-a",
                "category": "identity",
                "evidence_completeness_score": 40,
            },
        ]
    )

    assert summary.loc[0, "finding_count"] == 2
    assert summary.loc[0, "average_evidence_completeness_score"] == 60
    assert summary.loc[0, "weak_evidence_count"] == 1
