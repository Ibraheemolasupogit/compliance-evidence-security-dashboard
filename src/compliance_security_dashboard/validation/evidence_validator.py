"""Evidence validation helpers."""

EVIDENCE_FIELDS = (
    "evidence",
    "resource_id",
    "recommendation",
    "control_mapping",
    "remediation_owner",
)


def has_evidence_text(finding: dict[str, object]) -> bool:
    """Return True when a finding contains non-empty evidence text."""
    return bool(str(finding.get("evidence", "")).strip())


def evidence_field_status(finding: dict[str, object]) -> dict[str, bool]:
    """Return whether each evidence completeness field is present."""
    return {
        field_name: bool(str(finding.get(field_name, "")).strip())
        for field_name in EVIDENCE_FIELDS
    }
