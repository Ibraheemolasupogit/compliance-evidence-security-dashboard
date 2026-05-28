"""Placeholder source routing for offline finding files."""

from pathlib import Path

SOURCE_FILES = {
    "saas": Path("data/input/saas_findings.json"),
    "snowflake": Path("data/input/snowflake_findings.json"),
    "iam": Path("data/input/iam_findings.json"),
}


def get_source_path(source_name: str) -> Path:
    """Return the offline path for a configured source."""
    return SOURCE_FILES[source_name]
