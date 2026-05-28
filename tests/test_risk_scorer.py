from compliance_security_dashboard.scoring.risk_scorer import score_severity


def test_score_severity_high():
    assert score_severity("high") == 75
