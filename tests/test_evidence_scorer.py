from compliance_security_dashboard.scoring.evidence_scorer import score_evidence_quality


def test_score_evidence_quality_with_evidence():
    assert score_evidence_quality(True) == 100
