import json

import pandas as pd

from compliance_security_dashboard.ingestion.json_loader import load_json
from compliance_security_dashboard.main import run_pipeline
from compliance_security_dashboard.normalization.schema_normalizer import (
    normalize_finding,
)


def test_normalize_sample_source_findings():
    sample_cases = [
        (
            "saas",
            "data/input/saas_findings.json",
            "saas-security-posture-monitoring",
        ),
        (
            "snowflake",
            "data/input/snowflake_findings.json",
            "snowflake-data-platform-security-monitoring",
        ),
        (
            "iam",
            "data/input/iam_findings.json",
            "identity-access-governance-automation",
        ),
    ]

    for source_name, path, expected_repo in sample_cases:
        raw_finding = load_json(path)[0]
        unified = normalize_finding(
            raw_finding,
            source_name=source_name,
            source_path=path,
        )
        assert unified.finding_id
        assert unified.source_system == source_name
        assert unified.source_repo == expected_repo
        assert unified.due_date
        assert unified.remediation_owner


def test_run_pipeline_writes_unified_outputs(tmp_path):
    output_json = tmp_path / "unified_findings.json"
    output_csv = tmp_path / "unified_findings.csv"
    risk_summary_csv = tmp_path / "risk_score_summary.csv"
    evidence_summary_csv = tmp_path / "evidence_quality_summary.csv"
    control_mapping_summary_csv = tmp_path / "control_mapping_summary.csv"
    control_coverage_summary_csv = tmp_path / "control_coverage_summary.csv"
    unmapped_findings_csv = tmp_path / "unmapped_findings.csv"
    remediation_tracker_csv = tmp_path / "remediation_tracker.csv"
    remediation_summary_csv = tmp_path / "remediation_summary.csv"
    remediation_owner_summary_csv = tmp_path / "remediation_owner_summary.csv"
    overdue_findings_csv = tmp_path / "overdue_findings.csv"
    due_soon_findings_csv = tmp_path / "due_soon_findings.csv"
    validation_summary_json = tmp_path / "validation_summary.json"
    report_dir = tmp_path / "reports"
    report_paths = {
        "executive_summary.md.j2": report_dir / "executive_summary.md",
        "technical_report.md.j2": report_dir / "technical_report.md",
        "remediation_plan.md.j2": report_dir / "remediation_plan.md",
        "compliance_evidence_pack.md.j2": report_dir / "compliance_evidence_pack.md",
    }

    findings = run_pipeline(
        output_json_path=output_json,
        output_csv_path=output_csv,
        risk_summary_csv_path=risk_summary_csv,
        evidence_summary_csv_path=evidence_summary_csv,
        control_mapping_summary_csv_path=control_mapping_summary_csv,
        control_coverage_summary_csv_path=control_coverage_summary_csv,
        unmapped_findings_csv_path=unmapped_findings_csv,
        remediation_tracker_csv_path=remediation_tracker_csv,
        remediation_summary_csv_path=remediation_summary_csv,
        remediation_owner_summary_csv_path=remediation_owner_summary_csv,
        overdue_findings_csv_path=overdue_findings_csv,
        due_soon_findings_csv_path=due_soon_findings_csv,
        validation_summary_json_path=validation_summary_json,
        report_paths=report_paths,
    )

    assert len(findings) == 3
    assert output_json.exists()
    assert output_csv.exists()
    assert risk_summary_csv.exists()
    assert evidence_summary_csv.exists()
    assert control_mapping_summary_csv.exists()
    assert control_coverage_summary_csv.exists()
    assert unmapped_findings_csv.exists()
    assert remediation_tracker_csv.exists()
    assert remediation_summary_csv.exists()
    assert remediation_owner_summary_csv.exists()
    assert overdue_findings_csv.exists()
    assert due_soon_findings_csv.exists()
    assert validation_summary_json.exists()
    for report_path in report_paths.values():
        assert report_path.exists()

    json_records = json.loads(output_json.read_text(encoding="utf-8"))
    csv_records = pd.read_csv(output_csv)
    control_mapping_summary = pd.read_csv(control_mapping_summary_csv)
    control_coverage_summary = pd.read_csv(control_coverage_summary_csv)
    unmapped_findings = pd.read_csv(unmapped_findings_csv)
    remediation_tracker = pd.read_csv(remediation_tracker_csv)
    remediation_summary = pd.read_csv(remediation_summary_csv)
    remediation_owner_summary = pd.read_csv(remediation_owner_summary_csv)
    validation_summary = json.loads(validation_summary_json.read_text(encoding="utf-8"))

    assert len(json_records) == 3
    assert len(csv_records) == 3
    assert "evidence_completeness_score" in csv_records.columns
    assert "cis_control" in control_mapping_summary.columns
    assert control_coverage_summary.loc[0, "mapped_findings"] == 3
    assert "finding_id" in unmapped_findings.columns
    assert unmapped_findings.empty
    assert "sla_status" in remediation_tracker.columns
    assert "finding_count" in remediation_summary.columns
    assert "overdue_findings" in remediation_owner_summary.columns
    assert validation_summary["portfolio_risk_summary"]["total_findings"] == 3
    assert validation_summary["raw_findings"]["issue_count"] > 0

    assert "Executive Summary" in report_paths["executive_summary.md.j2"].read_text(
        encoding="utf-8"
    )
    assert "Technical Report" in report_paths["technical_report.md.j2"].read_text(
        encoding="utf-8"
    )
    assert "Remediation Plan" in report_paths["remediation_plan.md.j2"].read_text(
        encoding="utf-8"
    )
    assert "Compliance Evidence Pack" in report_paths[
        "compliance_evidence_pack.md.j2"
    ].read_text(encoding="utf-8")
