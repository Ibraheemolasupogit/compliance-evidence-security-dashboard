"""Markdown report rendering helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound


def render_markdown(template_text: str, context: dict[str, object]) -> str:
    """Render a Markdown report from a template string."""
    environment = Environment(autoescape=False, undefined=StrictUndefined)
    template = environment.from_string(template_text)
    return template.render(**context)


def load_template(template_name: str, template_dir: str | Path) -> Any:
    """Load a Jinja2 template by name."""
    template_path = Path(template_dir)
    if not template_path.exists():
        raise FileNotFoundError(f"Template directory not found: {template_path}")

    environment = Environment(
        loader=FileSystemLoader(template_path),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    try:
        return environment.get_template(template_name)
    except TemplateNotFound as error:
        raise FileNotFoundError(
            f"Markdown report template not found: {template_path / template_name}"
        ) from error


def render_template(
    template_name: str,
    context: dict[str, Any],
    template_dir: str | Path,
) -> str:
    """Render a named Markdown template."""
    return load_template(template_name, template_dir).render(**context)


def write_markdown_report(content: str, output_path: str | Path) -> Path:
    """Write Markdown content to disk."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def generate_markdown_report(
    template_name: str,
    context: dict[str, Any],
    output_path: str | Path,
    template_dir: str | Path,
) -> Path:
    """Render and write one Markdown report."""
    content = render_template(template_name, context, template_dir)
    return write_markdown_report(content, output_path)


def generate_all_reports(
    context: dict[str, Any],
    report_paths: dict[str, str | Path],
    template_dir: str | Path,
) -> list[Path]:
    """Generate all configured Markdown reports."""
    generated_paths = []
    for template_name, output_path in report_paths.items():
        generated_paths.append(
            generate_markdown_report(
                template_name=template_name,
                context=context,
                output_path=output_path,
                template_dir=template_dir,
            )
        )
    return generated_paths


def build_report_context(
    *,
    project_title: str,
    reporting_date: str,
    unified_findings: list[dict[str, Any]],
    risk_summary: pd.DataFrame,
    evidence_quality_summary: pd.DataFrame,
    control_mapping_summary: pd.DataFrame,
    control_coverage_summary: dict[str, Any],
    remediation_tracker: pd.DataFrame,
    remediation_owner_summary: pd.DataFrame,
    overdue_findings: pd.DataFrame,
    due_soon_findings: pd.DataFrame,
    validation_summary: dict[str, Any],
) -> dict[str, Any]:
    """Build report context from pipeline outputs."""
    portfolio_risk = validation_summary.get("portfolio_risk_summary", {})
    findings = sorted(
        unified_findings,
        key=lambda finding: int(finding.get("risk_score", 0)),
        reverse=True,
    )
    top_risks = findings[:5]
    high_critical = [
        finding
        for finding in findings
        if finding.get("severity") in {"High", "Critical"}
    ]

    return {
        "project_title": project_title,
        "reporting_date": reporting_date,
        "portfolio_risk": portfolio_risk,
        "total_findings": portfolio_risk.get("total_findings", len(findings)),
        "open_findings": portfolio_risk.get("open_findings", 0),
        "critical_findings": portfolio_risk.get("critical_findings", 0),
        "high_findings": portfolio_risk.get("high_findings", 0),
        "average_risk_score": portfolio_risk.get("average_risk_score", 0),
        "risk_rating": portfolio_risk.get("risk_rating", "Info"),
        "top_risk_score": portfolio_risk.get("top_risk_score", 0),
        "overdue_count": len(overdue_findings),
        "due_soon_count": len(due_soon_findings),
        "weak_evidence_count": count_weak_evidence(unified_findings),
        "average_evidence_completeness_score": average_field(
            unified_findings,
            "evidence_completeness_score",
        ),
        "control_coverage": control_coverage_summary,
        "top_risks": top_risks,
        "high_critical_findings": high_critical,
        "findings_table": dataframe_to_markdown(pd.DataFrame(findings)),
        "risk_summary_table": dataframe_to_markdown(risk_summary),
        "evidence_summary_table": dataframe_to_markdown(evidence_quality_summary),
        "control_mapping_table": dataframe_to_markdown(control_mapping_summary),
        "control_coverage_table": dataframe_to_markdown(
            pd.DataFrame([control_coverage_summary])
        ),
        "remediation_tracker_table": dataframe_to_markdown(remediation_tracker),
        "remediation_owner_table": dataframe_to_markdown(remediation_owner_summary),
        "overdue_findings_table": dataframe_to_markdown(overdue_findings),
        "due_soon_findings_table": dataframe_to_markdown(due_soon_findings),
        "unmapped_count": control_coverage_summary.get("unmapped_findings", 0),
        "validation_issue_count": validation_summary.get("raw_findings", {}).get(
            "issue_count",
            0,
        )
        + validation_summary.get("normalized_findings", {}).get("issue_count", 0),
    }


def dataframe_to_markdown(frame: pd.DataFrame, limit: int = 10) -> str:
    """Render a dataframe as a compact Markdown table."""
    if frame.empty:
        return "_No records._"
    limited = frame.head(limit).fillna("")
    headers = [str(column) for column in limited.columns]
    rows = [
        [str(value) for value in row]
        for row in limited.itertuples(index=False, name=None)
    ]
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join("---" for _ in headers) + " |"
    data_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *data_rows])


def average_field(records: list[dict[str, Any]], field_name: str) -> float:
    """Average a numeric field across records."""
    values = [float(record.get(field_name, 0) or 0) for record in records]
    return round(sum(values) / len(values), 2) if values else 0


def count_weak_evidence(records: list[dict[str, Any]]) -> int:
    """Count findings with weak evidence completeness."""
    return sum(
        1
        for record in records
        if int(record.get("evidence_completeness_score", 0)) < 60
    )
