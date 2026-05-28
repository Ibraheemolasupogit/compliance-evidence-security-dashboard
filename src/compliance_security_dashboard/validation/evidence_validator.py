"""Placeholder evidence validation."""


def has_evidence_text(finding: dict[str, object]) -> bool:
    """Return True when a finding contains non-empty evidence text."""
    return bool(str(finding.get("evidence", "")).strip())
