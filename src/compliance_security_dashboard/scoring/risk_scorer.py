"""Minimal risk scoring placeholder."""

SEVERITY_SCORES = {
    "critical": 100,
    "high": 75,
    "medium": 50,
    "low": 25,
    "informational": 5,
}


def score_severity(severity: str) -> int:
    """Return a baseline risk score for a severity."""
    return SEVERITY_SCORES.get(severity.lower(), 0)
