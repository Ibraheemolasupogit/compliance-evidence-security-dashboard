"""Minimal schema normalization placeholder."""

from typing import Any


def normalize_finding(raw_finding: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow normalized finding for the initial foundation."""
    return dict(raw_finding)
