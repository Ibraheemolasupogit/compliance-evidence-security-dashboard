"""Placeholder field mapping helpers."""


def map_severity(value: str) -> str:
    """Normalize severity text."""
    return value.strip().lower()
