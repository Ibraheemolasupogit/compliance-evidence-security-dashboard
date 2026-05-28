"""Evidence completeness scoring helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd

from compliance_security_dashboard.validation.evidence_validator import (
    EVIDENCE_FIELDS,
    evidence_field_status,
)


def score_evidence_quality(has_evidence: bool) -> int:
    """Return a simple evidence quality score."""
    return 100 if has_evidence else 0


def score_evidence_completeness(finding: dict[str, Any]) -> int:
    """Score evidence completeness as a percentage across required checks."""
    statuses = evidence_field_status(finding)
    present_count = sum(1 for present in statuses.values() if present)
    return round((present_count / len(EVIDENCE_FIELDS)) * 100)


def apply_evidence_scores(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add evidence completeness score to each finding."""
    enriched_findings = []
    for finding in findings:
        enriched = dict(finding)
        enriched["evidence_completeness_score"] = score_evidence_completeness(enriched)
        enriched_findings.append(enriched)
    return enriched_findings


def build_evidence_quality_summary(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build grouped evidence quality metrics."""
    columns = [
        "source_repo",
        "category",
        "finding_count",
        "average_evidence_completeness_score",
        "weak_evidence_count",
    ]
    if not findings:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(findings)
    frame["weak_evidence"] = frame["evidence_completeness_score"] < 60
    summary = (
        frame.groupby(["source_repo", "category"], dropna=False)
        .agg(
            finding_count=("finding_id", "count"),
            average_evidence_completeness_score=(
                "evidence_completeness_score",
                "mean",
            ),
            weak_evidence_count=("weak_evidence", "sum"),
        )
        .reset_index()
    )
    summary["average_evidence_completeness_score"] = summary[
        "average_evidence_completeness_score"
    ].round(2)
    return summary[columns]
