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

    findings = run_pipeline(output_json_path=output_json, output_csv_path=output_csv)

    assert len(findings) == 3
    assert output_json.exists()
    assert output_csv.exists()

    json_records = json.loads(output_json.read_text(encoding="utf-8"))
    csv_records = pd.read_csv(output_csv)

    assert len(json_records) == 3
    assert len(csv_records) == 3
    assert "evidence_completeness_score" in csv_records.columns
