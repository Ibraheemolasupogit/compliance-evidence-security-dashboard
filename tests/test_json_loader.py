import json

import pytest

from compliance_security_dashboard.ingestion.json_loader import load_json


def test_load_json_list(tmp_path):
    path = tmp_path / "findings.json"
    path.write_text(json.dumps([{"finding_id": "TEST-001"}]), encoding="utf-8")

    assert load_json(path) == [{"finding_id": "TEST-001"}]


def test_load_json_findings_dictionary(tmp_path):
    path = tmp_path / "findings.json"
    path.write_text(
        json.dumps({"findings": [{"finding_id": "TEST-001"}]}),
        encoding="utf-8",
    )

    assert load_json(path) == [{"finding_id": "TEST-001"}]


def test_load_json_rejects_unsupported_format(tmp_path):
    path = tmp_path / "findings.json"
    path.write_text(json.dumps({"items": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported JSON format"):
        load_json(path)
