from compliance_security_dashboard.scoring.risk_scorer import (
    build_portfolio_risk_summary,
    build_risk_summary,
    ensure_risk_score,
    score_severity,
)


def test_score_severity_high():
    assert score_severity("high") == 80


def test_ensure_risk_score_defaults_missing_score():
    finding = ensure_risk_score({"severity": "Critical", "risk_score": ""})

    assert finding["risk_score"] == 95


def test_build_risk_summary_dataframe():
    summary = build_risk_summary(
        [
            {
                "finding_id": "TEST-001",
                "source_repo": "repo-a",
                "severity": "High",
                "category": "identity",
                "risk_score": 80,
            },
            {
                "finding_id": "TEST-002",
                "source_repo": "repo-a",
                "severity": "High",
                "category": "identity",
                "risk_score": 90,
            },
        ]
    )

    assert summary.loc[0, "finding_count"] == 2
    assert summary.loc[0, "average_risk_score"] == 85
    assert summary.loc[0, "max_risk_score"] == 90


def test_build_portfolio_risk_summary():
    summary = build_portfolio_risk_summary(
        [
            {
                "finding_id": "TEST-001",
                "severity": "High",
                "status": "Open",
                "risk_score": 80,
            },
            {
                "finding_id": "TEST-002",
                "severity": "Critical",
                "status": "Remediated",
                "risk_score": 95,
            },
        ]
    )

    assert summary["total_findings"] == 2
    assert summary["open_findings"] == 1
    assert summary["critical_findings"] == 1
    assert summary["risk_rating"] == "High"
