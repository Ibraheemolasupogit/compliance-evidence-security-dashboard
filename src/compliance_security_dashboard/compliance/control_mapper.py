"""Placeholder control mapping logic."""


def map_control(category: str) -> str:
    """Return a sample control identifier for a category."""
    defaults = {
        "identity": "CTRL-IAM-001",
        "access_governance": "CTRL-DATA-002",
        "privileged_access": "CTRL-IAM-002",
    }
    return defaults.get(category, "CTRL-GEN-001")
