import json

import pandas as pd
from dashboard.dashboard_utils import (
    format_percentage,
    format_risk_score,
    load_csv_output,
    load_json_output,
    safe_metric_value,
    value_counts_frame,
)


def test_load_csv_output_reads_file(tmp_path):
    path = tmp_path / "output.csv"
    path.write_text("name,count\nA,1\n", encoding="utf-8")

    frame = load_csv_output(path)

    assert frame.loc[0, "name"] == "A"


def test_load_csv_output_missing_file_returns_empty_frame(tmp_path):
    assert load_csv_output(tmp_path / "missing.csv").empty


def test_load_json_output_reads_file(tmp_path):
    path = tmp_path / "output.json"
    path.write_text(json.dumps({"total": 3}), encoding="utf-8")

    assert load_json_output(path) == {"total": 3}


def test_load_json_output_missing_file_returns_empty_dict(tmp_path):
    assert load_json_output(tmp_path / "missing.json") == {}


def test_metric_formatting_helpers():
    assert safe_metric_value(12.30) == "12.3"
    assert format_percentage(99.95) == "100.0%"
    assert format_risk_score(80.0) == "80"


def test_value_counts_frame():
    frame = pd.DataFrame({"severity": ["High", "High", "Medium"]})

    counts = value_counts_frame(frame, "severity")

    assert counts.loc[0, "severity"] == "High"
    assert counts.loc[0, "finding_count"] == 2
