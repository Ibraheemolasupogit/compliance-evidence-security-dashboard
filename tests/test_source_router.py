import json

import pytest

from compliance_security_dashboard.ingestion.source_router import route_source_file


def test_route_source_file_loads_json(tmp_path):
    path = tmp_path / "findings.json"
    path.write_text(json.dumps([{"finding_id": "JSON-001"}]), encoding="utf-8")

    assert route_source_file(path) == [{"finding_id": "JSON-001"}]


def test_route_source_file_loads_csv(tmp_path):
    path = tmp_path / "findings.csv"
    path.write_text("finding_id,severity\nCSV-001,high\n", encoding="utf-8")

    assert route_source_file(path) == [{"finding_id": "CSV-001", "severity": "high"}]


def test_route_source_file_rejects_unsupported_extension(tmp_path):
    path = tmp_path / "findings.txt"
    path.write_text("finding_id=TXT-001", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported source file format"):
        route_source_file(path)
