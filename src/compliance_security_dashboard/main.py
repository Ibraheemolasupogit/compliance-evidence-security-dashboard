"""Offline ingestion and normalization pipeline entry point."""

from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from dateutil.tz import gettz

from compliance_security_dashboard.compliance.control_mapper import (
    apply_compliance_mappings,
    identify_unmapped_findings,
    load_category_mappings,
    load_controls_reference,
)
from compliance_security_dashboard.compliance.coverage_analyzer import (
    build_control_coverage_summary,
    build_control_mapping_summary,
)
from compliance_security_dashboard.ingestion.source_router import load_default_sources
from compliance_security_dashboard.normalization.field_mapper import (
    map_severity,
    map_status,
)
from compliance_security_dashboard.normalization.schema_normalizer import (
    normalize_findings,
)
from compliance_security_dashboard.remediation.remediation_tracker import (
    apply_sla_statuses,
    build_remediation_owner_summary,
    build_remediation_summary,
    build_remediation_tracker,
    filter_due_soon_findings,
    filter_overdue_findings,
)
from compliance_security_dashboard.reporting.csv_exporter import export_csv
from compliance_security_dashboard.reporting.json_exporter import export_json
from compliance_security_dashboard.reporting.markdown_reporter import (
    build_report_context,
    generate_all_reports,
)
from compliance_security_dashboard.scoring.evidence_scorer import (
    apply_evidence_scores,
    build_evidence_quality_summary,
)
from compliance_security_dashboard.scoring.risk_scorer import (
    apply_risk_scores,
    build_portfolio_risk_summary,
    build_risk_summary,
)
from compliance_security_dashboard.validation.finding_validator import (
    merge_validation_results,
    validate_findings,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"
RISK_SCORING_PATH = PROJECT_ROOT / "config" / "risk_scoring.yaml"
COMPLIANCE_MAPPING_PATH = PROJECT_ROOT / "config" / "compliance_mapping.yaml"
CONTROLS_REFERENCE_PATH = PROJECT_ROOT / "data" / "reference" / "controls_reference.csv"
CATEGORY_MAPPING_PATH = PROJECT_ROOT / "data" / "reference" / "category_mapping.csv"
UNIFIED_JSON_PATH = PROJECT_ROOT / "outputs" / "unified_findings.json"
UNIFIED_CSV_PATH = PROJECT_ROOT / "outputs" / "unified_findings.csv"
RISK_SUMMARY_CSV_PATH = PROJECT_ROOT / "outputs" / "risk_score_summary.csv"
EVIDENCE_SUMMARY_CSV_PATH = PROJECT_ROOT / "outputs" / "evidence_quality_summary.csv"
CONTROL_MAPPING_SUMMARY_CSV_PATH = (
    PROJECT_ROOT / "outputs" / "control_mapping_summary.csv"
)
CONTROL_COVERAGE_SUMMARY_CSV_PATH = (
    PROJECT_ROOT / "outputs" / "control_coverage_summary.csv"
)
UNMAPPED_FINDINGS_CSV_PATH = PROJECT_ROOT / "outputs" / "unmapped_findings.csv"
REMEDIATION_TRACKER_CSV_PATH = PROJECT_ROOT / "outputs" / "remediation_tracker.csv"
REMEDIATION_SUMMARY_CSV_PATH = PROJECT_ROOT / "outputs" / "remediation_summary.csv"
REMEDIATION_OWNER_SUMMARY_CSV_PATH = (
    PROJECT_ROOT / "outputs" / "remediation_owner_summary.csv"
)
OVERDUE_FINDINGS_CSV_PATH = PROJECT_ROOT / "outputs" / "overdue_findings.csv"
DUE_SOON_FINDINGS_CSV_PATH = PROJECT_ROOT / "outputs" / "due_soon_findings.csv"
VALIDATION_SUMMARY_JSON_PATH = PROJECT_ROOT / "outputs" / "validation_summary.json"
REPORT_TEMPLATE_DIR = (
    PROJECT_ROOT / "src" / "compliance_security_dashboard" / "reporting" / "templates"
)
EXECUTIVE_SUMMARY_REPORT_PATH = PROJECT_ROOT / "reports" / "executive_summary.md"
TECHNICAL_REPORT_PATH = PROJECT_ROOT / "reports" / "technical_report.md"
REMEDIATION_PLAN_REPORT_PATH = PROJECT_ROOT / "reports" / "remediation_plan.md"
COMPLIANCE_EVIDENCE_PACK_REPORT_PATH = (
    PROJECT_ROOT / "reports" / "compliance_evidence_pack.md"
)
REPORT_PATHS = {
    "executive_summary.md.j2": EXECUTIVE_SUMMARY_REPORT_PATH,
    "technical_report.md.j2": TECHNICAL_REPORT_PATH,
    "remediation_plan.md.j2": REMEDIATION_PLAN_REPORT_PATH,
    "compliance_evidence_pack.md.j2": COMPLIANCE_EVIDENCE_PACK_REPORT_PATH,
}


def load_settings(path: str | Path = SETTINGS_PATH) -> dict[str, Any]:
    """Load pipeline settings."""
    return load_yaml(path)


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML mapping from disk."""
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
    risk_summary_csv_path: str | Path = RISK_SUMMARY_CSV_PATH,
    evidence_summary_csv_path: str | Path = EVIDENCE_SUMMARY_CSV_PATH,
    control_mapping_summary_csv_path: str | Path = CONTROL_MAPPING_SUMMARY_CSV_PATH,
    control_coverage_summary_csv_path: str | Path = CONTROL_COVERAGE_SUMMARY_CSV_PATH,
    unmapped_findings_csv_path: str | Path = UNMAPPED_FINDINGS_CSV_PATH,
    remediation_tracker_csv_path: str | Path = REMEDIATION_TRACKER_CSV_PATH,
    remediation_summary_csv_path: str | Path = REMEDIATION_SUMMARY_CSV_PATH,
    remediation_owner_summary_csv_path: str | Path = REMEDIATION_OWNER_SUMMARY_CSV_PATH,
    overdue_findings_csv_path: str | Path = OVERDUE_FINDINGS_CSV_PATH,
    due_soon_findings_csv_path: str | Path = DUE_SOON_FINDINGS_CSV_PATH,
    validation_summary_json_path: str | Path = VALIDATION_SUMMARY_JSON_PATH,
    report_paths: dict[str, str | Path] | None = None,
    report_template_dir: str | Path = REPORT_TEMPLATE_DIR,
    settings_path: str | Path = SETTINGS_PATH,
    risk_scoring_path: str | Path = RISK_SCORING_PATH,
    compliance_mapping_path: str | Path = COMPLIANCE_MAPPING_PATH,
    controls_reference_path: str | Path = CONTROLS_REFERENCE_PATH,
    category_mapping_path: str | Path = CATEGORY_MAPPING_PATH,
) -> list[dict[str, Any]]:
    """Run offline ingestion, validation, scoring, and export."""
    settings = load_settings(settings_path)
    risk_config = load_yaml(risk_scoring_path)
    load_yaml(compliance_mapping_path)
    controls_reference = load_controls_reference(controls_reference_path)
    category_mappings = load_category_mappings(category_mapping_path)
    sla_days = settings.get("sla_days", {})
    severity_scores = risk_config.get("severity_weights", {})
    unified_findings = []
    raw_validation_results = []

    for source_name, source_path, raw_findings in load_default_sources():
        raw_validation_results.append(
            validate_findings(raw_findings, source=str(source_path))
        )
        normalized = normalize_findings(
            raw_findings,
            source_name=source_name,
            source_path=source_path,
            sla_days=sla_days,
        )
        unified_findings.extend(finding.to_dict() for finding in normalized)

    unified_findings = standardize_values(unified_findings)
    unified_findings = apply_risk_scores(unified_findings, severity_scores)
    unified_findings = apply_compliance_mappings(
        unified_findings,
        controls=controls_reference,
        category_mappings=category_mappings,
    )
    unified_findings = apply_evidence_scores(unified_findings)
    unified_findings = apply_sla_statuses(unified_findings)
    normalized_validation = validate_findings(unified_findings, source="normalized")
    risk_summary = build_risk_summary(unified_findings)
    evidence_summary = build_evidence_quality_summary(unified_findings)
    control_mapping_summary = build_control_mapping_summary(unified_findings)
    control_coverage_summary = build_control_coverage_summary(unified_findings)
    unmapped_findings = identify_unmapped_findings(unified_findings)
    unmapped_findings_export = pd.DataFrame(
        unmapped_findings,
        columns=unified_findings[0].keys() if unified_findings else None,
    )
    remediation_tracker = build_remediation_tracker(unified_findings)
    remediation_summary = build_remediation_summary(unified_findings)
    remediation_owner_summary = build_remediation_owner_summary(unified_findings)
    overdue_findings = filter_overdue_findings(unified_findings)
    due_soon_findings = filter_due_soon_findings(unified_findings)
    portfolio_risk_summary = build_portfolio_risk_summary(unified_findings)
    validation_summary = {
        "raw_findings": merge_validation_results(raw_validation_results),
        "normalized_findings": normalized_validation.to_dict(),
        "portfolio_risk_summary": portfolio_risk_summary,
    }
    report_context = build_report_context(
        project_title=settings.get("project", {}).get(
            "name",
            "compliance-evidence-security-dashboard",
        ),
        reporting_date=current_reporting_date(settings),
        unified_findings=unified_findings,
        risk_summary=risk_summary,
        evidence_quality_summary=evidence_summary,
        control_mapping_summary=control_mapping_summary,
        control_coverage_summary=control_coverage_summary,
        remediation_tracker=remediation_tracker,
        remediation_owner_summary=remediation_owner_summary,
        overdue_findings=overdue_findings,
        due_soon_findings=due_soon_findings,
        validation_summary=validation_summary,
    )

    export_json(unified_findings, output_json_path)
    export_csv(unified_findings, output_csv_path)
    export_csv(risk_summary, risk_summary_csv_path)
    export_csv(evidence_summary, evidence_summary_csv_path)
    export_csv(control_mapping_summary, control_mapping_summary_csv_path)
    export_csv(control_coverage_summary, control_coverage_summary_csv_path)
    export_csv(unmapped_findings_export, unmapped_findings_csv_path)
    export_csv(remediation_tracker, remediation_tracker_csv_path)
    export_csv(remediation_summary, remediation_summary_csv_path)
    export_csv(remediation_owner_summary, remediation_owner_summary_csv_path)
    export_csv(overdue_findings, overdue_findings_csv_path)
    export_csv(due_soon_findings, due_soon_findings_csv_path)
    export_json(validation_summary, validation_summary_json_path)
    generate_all_reports(
        context=report_context,
        report_paths=report_paths or REPORT_PATHS,
        template_dir=report_template_dir,
    )
    return unified_findings


def standardize_values(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Standardize severity and status fields for all findings."""
    standardized = []
    for finding in findings:
        updated = dict(finding)
        updated["severity"] = map_severity(str(updated.get("severity", "Info")))
        updated["status"] = map_status(str(updated.get("status", "Open")))
        standardized.append(updated)
    return standardized


def current_reporting_date(settings: dict[str, Any]) -> str:
    """Return the current report date using configured defaults."""
    from datetime import datetime

    defaults = settings.get("defaults", {})
    timezone_name = defaults.get("timezone", "UTC")
    date_format = defaults.get("date_format", "%Y-%m-%d")
    timezone = gettz(timezone_name)
    return datetime.now(tz=timezone).strftime(date_format)


def main() -> None:
    """Run the offline pipeline and print generated outputs."""
    findings = run_pipeline()
    print(f"Generated {len(findings)} unified findings.")
    print(f"Wrote {UNIFIED_JSON_PATH}")
    print(f"Wrote {UNIFIED_CSV_PATH}")
    print(f"Wrote {RISK_SUMMARY_CSV_PATH}")
    print(f"Wrote {EVIDENCE_SUMMARY_CSV_PATH}")
    print(f"Wrote {CONTROL_MAPPING_SUMMARY_CSV_PATH}")
    print(f"Wrote {CONTROL_COVERAGE_SUMMARY_CSV_PATH}")
    print(f"Wrote {UNMAPPED_FINDINGS_CSV_PATH}")
    print(f"Wrote {REMEDIATION_TRACKER_CSV_PATH}")
    print(f"Wrote {REMEDIATION_SUMMARY_CSV_PATH}")
    print(f"Wrote {REMEDIATION_OWNER_SUMMARY_CSV_PATH}")
    print(f"Wrote {OVERDUE_FINDINGS_CSV_PATH}")
    print(f"Wrote {DUE_SOON_FINDINGS_CSV_PATH}")
    print(f"Wrote {VALIDATION_SUMMARY_JSON_PATH}")
    print(f"Wrote {EXECUTIVE_SUMMARY_REPORT_PATH}")
    print(f"Wrote {TECHNICAL_REPORT_PATH}")
    print(f"Wrote {REMEDIATION_PLAN_REPORT_PATH}")
    print(f"Wrote {COMPLIANCE_EVIDENCE_PACK_REPORT_PATH}")


if __name__ == "__main__":
    main()
