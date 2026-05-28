"""Placeholder compliance coverage analysis."""


def count_mapped_controls(findings: list[dict[str, object]]) -> int:
    """Count findings with a mapped control identifier."""
    return sum(1 for finding in findings if finding.get("control_id"))
