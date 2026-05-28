"""Placeholder remediation tracking."""


def is_open_status(status: str) -> bool:
    """Return True for statuses that still require action."""
    return status in {"open", "in_progress", "deferred"}
