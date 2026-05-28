"""Risk scoring and summary helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd

from compliance_security_dashboard.normalization.field_mapper import map_severity

DEFAULT_SEVERITY_SCORES = {
    "Critical": 95,
    "High": 80,
    "Medium": 55,
    "Low": 25,
    "Info": 5,
}


def score_severity(
    severity: str,
    severity_scores: dict[str, int] | None = None,
) -> int:
    """Return a default risk score for a severity."""
    scores = severity_scores or DEFAULT_SEVERITY_SCORES
    return scores.get(map_severity(severity), DEFAULT_SEVERITY_SCORES["Info"])


def ensure_risk_score(
    finding: dict[str, Any],
    severity_scores: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Ensure a finding has a bounded integer risk score."""
    enriched = dict(finding)
    risk_score = enriched.get("risk_score")
    try:
        score = int(risk_score)
    except (TypeError, ValueError):
        score = score_severity(str(enriched.get("severity", "Info")), severity_scores)

    enriched["risk_score"] = max(0, min(score, 100))
    return enriched


def apply_risk_scores(
    findings: list[dict[str, Any]],
    severity_scores: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    """Apply default and bounded risk scores to findings."""
    return [ensure_risk_score(finding, severity_scores) for finding in findings]


def build_risk_summary(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build grouped risk score summary metrics."""
    columns = [
        "source_repo",
        "severity",
        "category",
        "finding_count",
        "average_risk_score",
        "max_risk_score",
    ]
    if not findings:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(findings)
    summary = (
        frame.groupby(["source_repo", "severity", "category"], dropna=False)
        .agg(
            finding_count=("finding_id", "count"),
            average_risk_score=("risk_score", "mean"),
            max_risk_score=("risk_score", "max"),
        )
        .reset_index()
    )
    summary["average_risk_score"] = summary["average_risk_score"].round(2)
    return summary[columns]


def build_portfolio_risk_summary(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Build portfolio-level risk summary metrics."""
    if not findings:
        return {
            "total_findings": 0,
            "open_findings": 0,
            "critical_findings": 0,
            "high_findings": 0,
            "average_risk_score": 0,
            "risk_rating": "Info",
            "top_risk_score": 0,
        }

    frame = pd.DataFrame(findings)
    average_score = float(frame["risk_score"].mean())
    top_score = int(frame["risk_score"].max())
    return {
        "total_findings": int(len(frame)),
        "open_findings": int((frame["status"] == "Open").sum()),
        "critical_findings": int((frame["severity"] == "Critical").sum()),
        "high_findings": int((frame["severity"] == "High").sum()),
        "average_risk_score": round(average_score, 2),
        "risk_rating": risk_rating(average_score),
        "top_risk_score": top_score,
    }


def risk_rating(score: float) -> str:
    """Convert an average risk score to a portfolio rating."""
    if score >= 90:
        return "Critical"
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    if score >= 10:
        return "Low"
    return "Info"
