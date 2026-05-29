"""Main Streamlit dashboard landing page."""

from __future__ import annotations

import streamlit as st

from dashboard.dashboard_utils import (
    first_record,
    format_percentage,
    format_risk_score,
    load_csv_output,
    load_json_output,
    output_path,
    render_missing_output_warning,
)

st.set_page_config(
    page_title="Compliance Evidence Security Dashboard",
    layout="wide",
)

st.title("Compliance Evidence Security Dashboard")
st.caption(
    "Offline portfolio dashboard for security findings, evidence, remediation, "
    "and compliance reporting."
)

required_outputs = [
    output_path("unified_findings.csv"),
    output_path("control_coverage_summary.csv"),
    output_path("evidence_quality_summary.csv"),
    output_path("remediation_tracker.csv"),
    output_path("validation_summary.json"),
]
render_missing_output_warning(required_outputs)

findings = load_csv_output(output_path("unified_findings.csv"))
coverage = first_record(load_csv_output(output_path("control_coverage_summary.csv")))
evidence_summary = load_csv_output(output_path("evidence_quality_summary.csv"))
remediation_tracker = load_csv_output(output_path("remediation_tracker.csv"))
validation_summary = load_json_output(output_path("validation_summary.json"))
portfolio_risk = (
    validation_summary.get("portfolio_risk_summary", {})
    if isinstance(validation_summary, dict)
    else {}
)

average_evidence = (
    evidence_summary["average_evidence_completeness_score"].mean()
    if not evidence_summary.empty
    and "average_evidence_completeness_score" in evidence_summary.columns
    else 0
)

metric_cols = st.columns(8)
metric_cols[0].metric("Findings", len(findings))
metric_cols[1].metric("Open", portfolio_risk.get("open_findings", 0))
metric_cols[2].metric("Critical", portfolio_risk.get("critical_findings", 0))
metric_cols[3].metric("High", portfolio_risk.get("high_findings", 0))
metric_cols[4].metric(
    "Avg Risk", format_risk_score(portfolio_risk.get("average_risk_score", 0))
)
metric_cols[5].metric(
    "Coverage", format_percentage(coverage.get("mapping_coverage_percent", 0))
)
metric_cols[6].metric("Avg Evidence", format_percentage(average_evidence))
metric_cols[7].metric(
    "Overdue",
    (
        int((remediation_tracker.get("sla_status") == "Overdue").sum())
        if not remediation_tracker.empty and "sla_status" in remediation_tracker
        else 0
    ),
)

st.subheader("What This Dashboard Shows")
st.write(
    "This dashboard turns offline sample findings from SaaS, Snowflake/data platform, "
    "and identity/access governance security projects into executive metrics, "
    "compliance coverage, remediation workload, technical findings, and evidence "
    "quality views."
)

st.subheader("Pages")
st.markdown(
    "- **Executive Overview:** risk posture, top risks, and business interpretation.\n"
    "- **Compliance View:** CIS/NIST/ISO-style mappings and control coverage.\n"
    "- **Remediation Tracker:** owner workload, SLA status, overdue, "
    "and due-soon work.\n"
    "- **Technical Findings:** filterable finding inventory for engineers.\n"
    "- **Evidence Quality:** evidence completeness and weak evidence tracking."
)

st.info(
    "Run `PYTHONPATH=src python3 -m compliance_security_dashboard.main` "
    "to refresh outputs before reviewing the dashboard."
)
