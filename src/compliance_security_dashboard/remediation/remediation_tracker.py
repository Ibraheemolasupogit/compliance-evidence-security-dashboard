"""Remediation tracking and summary helpers."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from compliance_security_dashboard.remediation.sla_calculator import (
    CLOSED_STATUSES,
    SLA_STATUS_DUE_SOON,
    SLA_STATUS_OVERDUE,
    calculate_sla_status,
)

REMEDIATION_TRACKER_COLUMNS = [
    "finding_id",
    "title",
    "severity",
    "risk_score",
    "source_repo",
    "source_system",
    "category",
    "cis_control",
    "nist_category",
    "iso_domain",
    "remediation_owner",
    "status",
    "due_date",
    "sla_status",
    "recommendation",
    "evidence_completeness_score",
]


def is_open_status(status: str) -> bool:
    """Return True for statuses that still require action."""
    return status not in CLOSED_STATUSES


def apply_sla_statuses(
    findings: list[dict[str, Any]],
    today: date | None = None,
) -> list[dict[str, Any]]:
    """Apply SLA status to each finding."""
    return [apply_sla_status(finding, today=today) for finding in findings]


def apply_sla_status(
    finding: dict[str, Any],
    today: date | None = None,
) -> dict[str, Any]:
    """Apply SLA status to a single finding."""
    enriched = dict(finding)
    enriched["sla_status"] = calculate_sla_status(
        due_date=enriched.get("due_date"),
        status=str(enriched.get("status", "")),
        severity=str(enriched.get("severity", "")),
        today=today,
    )
    return enriched


def build_remediation_tracker(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build the remediation tracker export."""
    frame = pd.DataFrame(findings)
    if frame.empty:
        return pd.DataFrame(columns=REMEDIATION_TRACKER_COLUMNS)

    for column in REMEDIATION_TRACKER_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    return frame[REMEDIATION_TRACKER_COLUMNS]


def build_remediation_summary(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build grouped remediation metrics."""
    columns = [
        "remediation_owner",
        "status",
        "severity",
        "sla_status",
        "finding_count",
        "average_risk_score",
        "max_risk_score",
        "average_evidence_completeness_score",
    ]
    if not findings:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(findings)
    summary = (
        frame.groupby(
            ["remediation_owner", "status", "severity", "sla_status"],
            dropna=False,
        )
        .agg(
            finding_count=("finding_id", "count"),
            average_risk_score=("risk_score", "mean"),
            max_risk_score=("risk_score", "max"),
            average_evidence_completeness_score=(
                "evidence_completeness_score",
                "mean",
            ),
        )
        .reset_index()
    )
    summary["average_risk_score"] = summary["average_risk_score"].round(2)
    summary["average_evidence_completeness_score"] = summary[
        "average_evidence_completeness_score"
    ].round(2)
    return summary[columns]


def build_remediation_owner_summary(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build remediation workload metrics by owner."""
    columns = [
        "remediation_owner",
        "total_findings",
        "open_findings",
        "overdue_findings",
        "due_soon_findings",
        "high_or_critical_findings",
        "average_risk_score",
        "average_evidence_completeness_score",
    ]
    if not findings:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(findings)
    frame["open_flag"] = ~frame["status"].isin(CLOSED_STATUSES)
    frame["overdue_flag"] = frame["sla_status"] == SLA_STATUS_OVERDUE
    frame["due_soon_flag"] = frame["sla_status"] == SLA_STATUS_DUE_SOON
    frame["high_or_critical_flag"] = frame["severity"].isin({"High", "Critical"})

    summary = (
        frame.groupby(["remediation_owner"], dropna=False)
        .agg(
            total_findings=("finding_id", "count"),
            open_findings=("open_flag", "sum"),
            overdue_findings=("overdue_flag", "sum"),
            due_soon_findings=("due_soon_flag", "sum"),
            high_or_critical_findings=("high_or_critical_flag", "sum"),
            average_risk_score=("risk_score", "mean"),
            average_evidence_completeness_score=(
                "evidence_completeness_score",
                "mean",
            ),
        )
        .reset_index()
    )
    summary["average_risk_score"] = summary["average_risk_score"].round(2)
    summary["average_evidence_completeness_score"] = summary[
        "average_evidence_completeness_score"
    ].round(2)
    return summary[columns]


def filter_overdue_findings(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Return overdue findings as remediation tracker rows."""
    return filter_findings_by_sla_status(findings, SLA_STATUS_OVERDUE)


def filter_due_soon_findings(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Return due-soon findings as remediation tracker rows."""
    return filter_findings_by_sla_status(findings, SLA_STATUS_DUE_SOON)


def filter_findings_by_sla_status(
    findings: list[dict[str, Any]],
    sla_status: str,
) -> pd.DataFrame:
    """Filter findings by SLA status and return tracker columns."""
    filtered = [
        finding for finding in findings if finding.get("sla_status") == sla_status
    ]
    return build_remediation_tracker(filtered)
