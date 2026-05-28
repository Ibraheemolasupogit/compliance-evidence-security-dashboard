"""Offline compliance control mapping logic."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from compliance_security_dashboard.ingestion.csv_loader import load_csv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONTROLS_PATH = PROJECT_ROOT / "data" / "reference" / "controls_reference.csv"
DEFAULT_CATEGORY_MAPPING_PATH = (
    PROJECT_ROOT / "data" / "reference" / "category_mapping.csv"
)

MAPPING_FIELDS = ("control_mapping", "cis_control", "nist_category", "iso_domain")


def load_controls_reference(path: str | Path = DEFAULT_CONTROLS_PATH) -> pd.DataFrame:
    """Load offline controls reference data."""
    return load_csv(path).fillna("")


def load_category_mappings(
    path: str | Path = DEFAULT_CATEGORY_MAPPING_PATH,
) -> pd.DataFrame:
    """Load offline category-to-control mapping data."""
    return load_csv(path).fillna("")


def map_control(category: str) -> str:
    """Return the default control identifier for a category."""
    mappings = load_category_mappings()
    match = mappings[mappings["source_category"] == category]
    if match.empty:
        return ""
    return str(match.iloc[0].get("default_control_id", ""))


def apply_compliance_mappings(
    findings: list[dict[str, Any]],
    controls: pd.DataFrame | None = None,
    category_mappings: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    """Apply offline compliance mappings to findings by category."""
    controls_frame = controls if controls is not None else load_controls_reference()
    mappings_frame = (
        category_mappings if category_mappings is not None else load_category_mappings()
    )
    mapped_findings = []

    for finding in findings:
        mapped_findings.append(
            apply_compliance_mapping(finding, controls_frame, mappings_frame)
        )

    return mapped_findings


def apply_compliance_mapping(
    finding: dict[str, Any],
    controls: pd.DataFrame,
    category_mappings: pd.DataFrame,
) -> dict[str, Any]:
    """Apply one compliance mapping, preserving explicit existing values."""
    mapped = dict(finding)
    category = str(mapped.get("category", ""))
    mapping = find_category_mapping(category, category_mappings)

    if mapping:
        set_if_blank(mapped, "control_mapping", mapping.get("default_control_id", ""))
        set_if_blank(mapped, "cis_control", mapping.get("cis_control", ""))
        set_if_blank(mapped, "nist_category", mapping.get("nist_category", ""))
        set_if_blank(mapped, "iso_domain", mapping.get("iso_domain", ""))
        set_if_blank(mapped, "control_theme", mapping.get("control_theme", ""))

    control_id = str(mapped.get("control_mapping", ""))
    control = find_control(control_id, controls)
    if control:
        set_if_blank(mapped, "cis_control", control.get("cis_control", ""))
        set_if_blank(mapped, "nist_category", control.get("nist_category", ""))
        set_if_blank(mapped, "iso_domain", control.get("iso_domain", ""))
        set_if_blank(mapped, "control_theme", control.get("control_family", ""))

    mapped["is_mapped"] = is_mapped_finding(mapped)
    return mapped


def find_category_mapping(
    category: str,
    category_mappings: pd.DataFrame,
) -> dict[str, Any] | None:
    """Find mapping metadata for a source or normalized category."""
    if category_mappings.empty:
        return None

    category_text = category.strip()
    matches = category_mappings[
        (category_mappings["source_category"] == category_text)
        | (category_mappings["normalized_category"] == category_text)
    ]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def find_control(control_id: str, controls: pd.DataFrame) -> dict[str, Any] | None:
    """Find control metadata by control identifier."""
    if not control_id or controls.empty:
        return None
    matches = controls[controls["control_id"] == control_id]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def set_if_blank(record: dict[str, Any], field_name: str, value: Any) -> None:
    """Set a field only when currently blank."""
    if record.get(field_name) in (None, "") and value not in (None, ""):
        record[field_name] = str(value)


def is_mapped_finding(finding: dict[str, Any]) -> bool:
    """Return True when a finding has any compliance framework mapping."""
    return any(
        str(finding.get(field_name, "")).strip() for field_name in MAPPING_FIELDS
    )


def identify_unmapped_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return findings missing CIS, NIST, and ISO mapping fields."""
    return [
        finding
        for finding in findings
        if not any(
            str(finding.get(field_name, "")).strip()
            for field_name in ("cis_control", "nist_category", "iso_domain")
        )
    ]
