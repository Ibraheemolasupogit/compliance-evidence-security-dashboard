"""Route offline source files to the correct loader."""

from pathlib import Path
from typing import Any

from compliance_security_dashboard.ingestion.csv_loader import load_csv_records
from compliance_security_dashboard.ingestion.json_loader import load_json

SOURCE_FILES = {
    "saas": Path("data/input/saas_findings.json"),
    "snowflake": Path("data/input/snowflake_findings.json"),
    "iam": Path("data/input/iam_findings.json"),
}


def get_source_path(source_name: str) -> Path:
    """Return the offline path for a configured source."""
    try:
        return SOURCE_FILES[source_name]
    except KeyError as error:
        known_sources = ", ".join(sorted(SOURCE_FILES))
        raise KeyError(
            f"Unknown source '{source_name}'. Known sources: {known_sources}"
        ) from error


def route_source_file(path: str | Path) -> list[dict[str, Any]]:
    """Load a source file by extension."""
    source_path = Path(path)
    suffix = source_path.suffix.lower()

    if suffix == ".json":
        return load_json(source_path)
    if suffix == ".csv":
        return load_csv_records(source_path)

    raise ValueError(
        f"Unsupported source file format '{suffix}' for {source_path}. "
        "Supported formats: .json, .csv"
    )


def load_default_sources() -> list[tuple[str, Path, list[dict[str, Any]]]]:
    """Load all default offline sources."""
    return [
        (source_name, source_path, route_source_file(source_path))
        for source_name, source_path in SOURCE_FILES.items()
    ]
