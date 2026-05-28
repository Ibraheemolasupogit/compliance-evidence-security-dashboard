"""Offline ingestion and normalization pipeline entry point."""

from pathlib import Path
from typing import Any

import yaml

from compliance_security_dashboard.ingestion.source_router import load_default_sources
from compliance_security_dashboard.normalization.schema_normalizer import (
    normalize_findings,
)
from compliance_security_dashboard.reporting.csv_exporter import export_csv
from compliance_security_dashboard.reporting.json_exporter import export_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"
UNIFIED_JSON_PATH = PROJECT_ROOT / "outputs" / "unified_findings.json"
UNIFIED_CSV_PATH = PROJECT_ROOT / "outputs" / "unified_findings.csv"


def load_settings(path: str | Path = SETTINGS_PATH) -> dict[str, Any]:
    """Load pipeline settings."""
    settings_path = Path(path)
    if not settings_path.exists():
        raise FileNotFoundError(f"Settings file not found: {settings_path}")
    with settings_path.open(encoding="utf-8") as file:
        settings = yaml.safe_load(file) or {}
    if not isinstance(settings, dict):
        raise ValueError(f"Settings file must contain a mapping: {settings_path}")
    return settings


def run_pipeline(
    output_json_path: str | Path = UNIFIED_JSON_PATH,
    output_csv_path: str | Path = UNIFIED_CSV_PATH,
    settings_path: str | Path = SETTINGS_PATH,
) -> list[dict[str, Any]]:
    """Run offline ingestion, normalization, and export."""
    settings = load_settings(settings_path)
    sla_days = settings.get("sla_days", {})
    unified_findings = []

    for source_name, source_path, raw_findings in load_default_sources():
        normalized = normalize_findings(
            raw_findings,
            source_name=source_name,
            source_path=source_path,
            sla_days=sla_days,
        )
        unified_findings.extend(finding.to_dict() for finding in normalized)

    export_json(unified_findings, output_json_path)
    export_csv(unified_findings, output_csv_path)
    return unified_findings


def main() -> None:
    """Run the offline pipeline and print generated outputs."""
    findings = run_pipeline()
    print(f"Generated {len(findings)} unified findings.")
    print(f"Wrote {UNIFIED_JSON_PATH}")
    print(f"Wrote {UNIFIED_CSV_PATH}")


if __name__ == "__main__":
    main()
