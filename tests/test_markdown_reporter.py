import pandas as pd
import pytest

from compliance_security_dashboard.reporting.markdown_reporter import (
    build_report_context,
    generate_markdown_report,
    load_template,
    render_markdown,
    write_markdown_report,
)


def test_load_template(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "sample.md.j2").write_text("# {{ title }}", encoding="utf-8")

    template = load_template("sample.md.j2", template_dir)

    assert template.render(title="Report") == "# Report"


def test_load_template_missing_file(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    with pytest.raises(FileNotFoundError, match="Markdown report template not found"):
        load_template("missing.md.j2", template_dir)


def test_render_markdown_from_simple_context():
    assert render_markdown("# {{ title }}", {"title": "Report"}) == "# Report"


def test_write_markdown_report(tmp_path):
    output_path = tmp_path / "reports" / "report.md"

    written_path = write_markdown_report("# Report", output_path)

    assert written_path == output_path
    assert output_path.read_text(encoding="utf-8") == "# Report\n"


def test_generate_markdown_report(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    output_path = tmp_path / "reports" / "report.md"
    (template_dir / "sample.md.j2").write_text("# {{ title }}", encoding="utf-8")

    generate_markdown_report(
        template_name="sample.md.j2",
        context={"title": "Generated"},
        output_path=output_path,
        template_dir=template_dir,
    )

    assert output_path.read_text(encoding="utf-8") == "# Generated\n"


def test_build_report_context():
    findings = [
        {
            "finding_id": "TEST-001",
            "title": "Finding",
            "severity": "High",
            "risk_score": 80,
            "evidence_completeness_score": 80,
        }
    ]
    context = build_report_context(
        project_title="Project",
        reporting_date="2026-05-28",
        unified_findings=findings,
        risk_summary=pd.DataFrame(),
        evidence_quality_summary=pd.DataFrame(),
        control_mapping_summary=pd.DataFrame(),
        control_coverage_summary={"mapping_coverage_percent": 100},
        remediation_tracker=pd.DataFrame(),
        remediation_owner_summary=pd.DataFrame(),
        overdue_findings=pd.DataFrame(),
        due_soon_findings=pd.DataFrame(),
        validation_summary={"portfolio_risk_summary": {"total_findings": 1}},
    )

    assert context["project_title"] == "Project"
    assert context["total_findings"] == 1
    assert context["top_risks"][0]["finding_id"] == "TEST-001"
