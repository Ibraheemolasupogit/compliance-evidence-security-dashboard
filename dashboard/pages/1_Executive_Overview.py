"""Executive overview dashboard page."""

from __future__ import annotations

import streamlit as st
from dashboard.dashboard_utils import (
    format_risk_score,
    load_csv_output,
    load_json_output,
    output_path,
    render_bar_chart,
    render_missing_output_warning,
    value_counts_frame,
)

st.set_page_config(page_title="Executive Overview", layout="wide")
st.title("Executive Overview")

required_outputs = [
    output_path("unified_findings.csv"),
    output_path("remediation_tracker.csv"),
    output_path("validation_summary.json"),
]
render_missing_output_warning(required_outputs)

findings = load_csv_output(output_path("unified_findings.csv"))
remediation = load_csv_output(output_path("remediation_tracker.csv"))
validation_summary = load_json_output(output_path("validation_summary.json"))
portfolio_risk = (
    validation_summary.get("portfolio_risk_summary", {})
    if isinstance(validation_summary, dict)
    else {}
)

metric_cols = st.columns(6)
metric_cols[0].metric("Total Findings", len(findings))
metric_cols[1].metric("Open", portfolio_risk.get("open_findings", 0))
metric_cols[2].metric("Critical", portfolio_risk.get("critical_findings", 0))
metric_cols[3].metric("High", portfolio_risk.get("high_findings", 0))
metric_cols[4].metric(
    "Avg Risk", format_risk_score(portfolio_risk.get("average_risk_score", 0))
)
metric_cols[5].metric("Risk Rating", portfolio_risk.get("risk_rating", "Info"))

sla_cols = st.columns(2)
sla_cols[0].metric(
    "Overdue",
    (
        int((remediation.get("sla_status") == "Overdue").sum())
        if not remediation.empty and "sla_status" in remediation
        else 0
    ),
)
sla_cols[1].metric(
    "Due Soon",
    (
        int((remediation.get("sla_status") == "Due Soon").sum())
        if not remediation.empty and "sla_status" in remediation
        else 0
    ),
)

chart_cols = st.columns(3)
with chart_cols[0]:
    render_bar_chart(
        value_counts_frame(findings, "severity"),
        x="severity",
        y="finding_count",
        title="Findings By Severity",
    )
with chart_cols[1]:
    render_bar_chart(
        value_counts_frame(findings, "source_repo"),
        x="source_repo",
        y="finding_count",
        title="Findings By Source Repo",
    )
with chart_cols[2]:
    render_bar_chart(
        value_counts_frame(findings, "category"),
        x="category",
        y="finding_count",
        title="Findings By Category",
    )

st.subheader("Top 10 Risks")
if findings.empty:
    st.info("No findings available.")
else:
    top_risks = findings.sort_values("risk_score", ascending=False).head(10)
    st.dataframe(
        top_risks[
            [
                "finding_id",
                "title",
                "severity",
                "risk_score",
                "source_repo",
                "remediation_owner",
                "sla_status",
            ]
        ],
        width="stretch",
    )

st.subheader("Executive Interpretation")
st.write(
    "The dashboard summarizes offline findings from SaaS, Snowflake/data platform, "
    "and IAM monitoring into a management view of risk, ownership, SLA pressure, "
    "and compliance coverage. Prioritize overdue high-risk findings and due-soon "
    "items before expanding control evidence depth."
)
