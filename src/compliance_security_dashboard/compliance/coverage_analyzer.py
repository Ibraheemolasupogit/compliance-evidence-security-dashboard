"""Compliance control coverage analysis."""

from __future__ import annotations

from typing import Any

import pandas as pd

from compliance_security_dashboard.compliance.control_mapper import (
    identify_unmapped_findings,
    is_mapped_finding,
)


def count_mapped_controls(findings: list[dict[str, object]]) -> int:
    """Count findings with a mapped control identifier."""
    return sum(1 for finding in findings if finding.get("control_mapping"))


def build_control_mapping_summary(findings: list[dict[str, Any]]) -> pd.DataFrame:
    """Build grouped compliance control mapping summary metrics."""
    columns = [
        "cis_control",
        "nist_category",
        "iso_domain",
        "category",
        "severity",
        "finding_count",
        "average_risk_score",
        "max_risk_score",
        "open_findings",
        "average_evidence_completeness_score",
    ]
    if not findings:
        return pd.DataFrame(columns=columns)

    frame = pd.DataFrame(findings)
    frame["open_flag"] = frame["status"] == "Open"
    summary = (
        frame.groupby(
            ["cis_control", "nist_category", "iso_domain", "category", "severity"],
            dropna=False,
        )
        .agg(
            finding_count=("finding_id", "count"),
            average_risk_score=("risk_score", "mean"),
            max_risk_score=("risk_score", "max"),
            open_findings=("open_flag", "sum"),
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


def build_control_coverage_summary(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Build portfolio-level compliance mapping coverage metrics."""
    total_findings = len(findings)
    mapped_findings = sum(1 for finding in findings if is_mapped_finding(finding))
    unmapped_findings = len(identify_unmapped_findings(findings))
    controls_with_findings = len(
        {
            finding.get("control_mapping")
            for finding in findings
            if str(finding.get("control_mapping", "")).strip()
        }
    )
    high_or_critical_control_findings = sum(
        1
        for finding in findings
        if finding.get("severity") in {"High", "Critical"}
        and is_mapped_finding(finding)
    )
    weak_evidence_control_findings = sum(
        1
        for finding in findings
        if is_mapped_finding(finding)
        and int(finding.get("evidence_completeness_score", 0)) < 60
    )

    coverage_percent = (
        round((mapped_findings / total_findings) * 100, 2) if total_findings else 0
    )

    return {
        "total_findings": total_findings,
        "mapped_findings": mapped_findings,
        "unmapped_findings": unmapped_findings,
        "mapping_coverage_percent": coverage_percent,
        "controls_with_findings": controls_with_findings,
        "high_or_critical_control_findings": high_or_critical_control_findings,
        "weak_evidence_control_findings": weak_evidence_control_findings,
    }
