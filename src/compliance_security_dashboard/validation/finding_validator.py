"""Minimal finding validation."""

REQUIRED_FINDING_FIELDS = {
    "finding_id",
    "source_system",
    "title",
    "severity",
    "category",
    "owner",
    "status",
}


def validate_required_fields(finding: dict[str, object]) -> bool:
    """Return True when the finding has the required foundation fields."""
    return REQUIRED_FINDING_FIELDS.issubset(finding)
