"""Field mapping helpers for source findings."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any


def map_severity(value: str) -> str:
    """Normalize severity text."""
    severity = str(value or "informational").strip().lower()
    aliases = {"info": "informational", "medium-high": "high"}
    return aliases.get(severity, severity)


def first_present(
    raw_finding: dict[str, Any],
    keys: tuple[str, ...],
    default: str = "",
) -> str:
    """Return the first non-empty field value from a raw finding."""
    for key in keys:
        value = raw_finding.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def infer_source_system(
    raw_finding: dict[str, Any],
    source_name: str | None = None,
) -> str:
    """Infer the source system from the record or configured source name."""
    return first_present(
        raw_finding,
        ("source_system", "source"),
        source_name or "unknown",
    )


def infer_source_repo(source_system: str, source_path: str | Path | None = None) -> str:
    """Infer the upstream portfolio repository for a source system."""
    repo_map = {
        "saas": "saas-security-posture-monitoring",
        "snowflake": "snowflake-data-platform-security-monitoring",
        "iam": "identity-access-governance-automation",
    }
    if source_system in repo_map:
        return repo_map[source_system]
    if source_path:
        return Path(source_path).stem
    return "unknown"


def map_risk_score(severity: str) -> int:
    """Return a simple baseline risk score from severity."""
    scores = {
        "critical": 100,
        "high": 75,
        "medium": 50,
        "low": 25,
        "informational": 5,
    }
    return scores.get(severity, 0)


def calculate_due_date(created_at: str, severity: str, sla_days: dict[str, int]) -> str:
    """Calculate a due date from the created date and severity SLA."""
    if not created_at:
        return ""
    created_date = date.fromisoformat(created_at[:10])
    days = sla_days.get(severity, sla_days.get("informational", 180))
    return (created_date + timedelta(days=days)).isoformat()


def map_default_control(category: str) -> str:
    """Map a normalized category to a simple control identifier."""
    control_map = {
        "identity": "CTRL-IAM-001",
        "access_governance": "CTRL-DATA-002",
        "privileged_access": "CTRL-IAM-002",
    }
    return control_map.get(category, "CTRL-GEN-001")


def map_cis_control(category: str) -> str:
    """Map category to a CIS-style placeholder control."""
    cis_map = {
        "identity": "CIS 6",
        "access_governance": "CIS 5",
        "privileged_access": "CIS 6",
    }
    return cis_map.get(category, "CIS TBD")


def map_nist_category(category: str) -> str:
    """Map category to a NIST-style placeholder category."""
    nist_map = {
        "identity": "PR.AC",
        "access_governance": "PR.AC",
        "privileged_access": "PR.AC",
    }
    return nist_map.get(category, "ID.RA")


def map_iso_domain(category: str) -> str:
    """Map category to an ISO-style placeholder domain."""
    iso_map = {
        "identity": "Access Control",
        "access_governance": "Access Control",
        "privileged_access": "Access Control",
    }
    return iso_map.get(category, "Security Governance")
