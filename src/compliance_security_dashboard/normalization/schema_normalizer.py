"""Normalize raw source findings into the unified finding schema."""

from pathlib import Path
from typing import Any

from compliance_security_dashboard.models.finding import UnifiedFinding
from compliance_security_dashboard.normalization.field_mapper import (
    calculate_due_date,
    first_present,
    infer_source_repo,
    infer_source_system,
    map_cis_control,
    map_default_control,
    map_iso_domain,
    map_nist_category,
    map_risk_score,
    map_severity,
    map_status,
)
from compliance_security_dashboard.scoring.risk_scorer import ensure_risk_score

DEFAULT_SLA_DAYS = {
    "Critical": 7,
    "High": 14,
    "Medium": 30,
    "Low": 90,
    "Info": 180,
}


def normalize_finding(
    raw_finding: dict[str, Any],
    source_name: str | None = None,
    source_path: str | Path | None = None,
    sla_days: dict[str, int] | None = None,
) -> UnifiedFinding:
    """Normalize one raw source finding into a UnifiedFinding."""
    severity = map_severity(first_present(raw_finding, ("severity",), "informational"))
    source_system = infer_source_system(raw_finding, source_name)
    category = first_present(
        raw_finding,
        ("category", "finding_category"),
        "uncategorized",
    )
    created_at = first_present(
        raw_finding,
        ("created_at", "observed_at", "detected_at"),
    )
    updated_at = first_present(
        raw_finding,
        ("updated_at", "observed_at", "detected_at"),
        created_at,
    )
    active_sla_days = sla_days or DEFAULT_SLA_DAYS
    evidence = first_present(raw_finding, ("evidence", "evidence_summary"))
    status = map_status(first_present(raw_finding, ("status",), "Open"))

    risk_seed = ensure_risk_score(
        {
            "risk_score": raw_finding.get("risk_score"),
            "severity": severity,
        }
    )

    return UnifiedFinding(
        finding_id=first_present(raw_finding, ("finding_id", "id"), "UNKNOWN"),
        source_system=source_system,
        source_repo=first_present(
            raw_finding,
            ("source_repo", "repository"),
            infer_source_repo(source_system, source_path),
        ),
        title=first_present(raw_finding, ("title", "name"), "Untitled finding"),
        description=first_present(raw_finding, ("description", "details"), ""),
        resource_type=first_present(raw_finding, ("resource_type", "asset_type"), ""),
        resource_name=first_present(
            raw_finding,
            ("resource_name", "asset_name", "resource"),
            "",
        ),
        resource_id=first_present(raw_finding, ("resource_id", "asset_id"), ""),
        category=category,
        severity=severity,
        risk_score=int(risk_seed.get("risk_score") or map_risk_score(severity)),
        control_mapping=first_present(
            raw_finding,
            ("control_mapping", "control_id"),
            map_default_control(category),
        ),
        cis_control=first_present(
            raw_finding,
            ("cis_control",),
            map_cis_control(category),
        ),
        nist_category=first_present(
            raw_finding,
            ("nist_category",),
            map_nist_category(category),
        ),
        iso_domain=first_present(
            raw_finding,
            ("iso_domain",),
            map_iso_domain(category),
        ),
        evidence=evidence,
        recommendation=first_present(
            raw_finding,
            ("recommendation", "remediation"),
            "Review finding and apply documented remediation.",
        ),
        remediation_owner=first_present(
            raw_finding,
            ("remediation_owner", "owner"),
            "Unassigned",
        ),
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        due_date=first_present(
            raw_finding,
            ("due_date",),
            calculate_due_date(created_at, severity, active_sla_days),
        ),
        sla_status=first_present(raw_finding, ("sla_status",), "not_evaluated"),
        evidence_completeness_score=int(
            raw_finding.get("evidence_completeness_score")
            if raw_finding.get("evidence_completeness_score") is not None
            else 100 if evidence else 0
        ),
    )


def normalize_findings(
    raw_findings: list[dict[str, Any]],
    source_name: str | None = None,
    source_path: str | Path | None = None,
    sla_days: dict[str, int] | None = None,
) -> list[UnifiedFinding]:
    """Normalize a collection of raw findings."""
    return [
        normalize_finding(
            raw_finding,
            source_name=source_name,
            source_path=source_path,
            sla_days=sla_days,
        )
        for raw_finding in raw_findings
    ]
