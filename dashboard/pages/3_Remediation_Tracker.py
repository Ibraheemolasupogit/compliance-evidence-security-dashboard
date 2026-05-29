"""Remediation tracker dashboard page."""

from __future__ import annotations

import streamlit as st
from dashboard.dashboard_utils import (
    load_csv_output,
    output_path,
    render_bar_chart,
    render_missing_output_warning,
    value_counts_frame,
)

st.set_page_config(page_title="Remediation Tracker", layout="wide")
st.title("Remediation Tracker")

required_outputs = [
    output_path("remediation_tracker.csv"),
    output_path("remediation_summary.csv"),
    output_path("remediation_owner_summary.csv"),
    output_path("overdue_findings.csv"),
    output_path("due_soon_findings.csv"),
]
render_missing_output_warning(required_outputs)

tracker = load_csv_output(output_path("remediation_tracker.csv"))
summary = load_csv_output(output_path("remediation_summary.csv"))
owner_summary = load_csv_output(output_path("remediation_owner_summary.csv"))
overdue = load_csv_output(output_path("overdue_findings.csv"))
due_soon = load_csv_output(output_path("due_soon_findings.csv"))

metric_cols = st.columns(5)
metric_cols[0].metric("Tracked Findings", len(tracker))
metric_cols[1].metric("Overdue", len(overdue))
metric_cols[2].metric("Due Soon", len(due_soon))
metric_cols[3].metric(
    "Owners",
    (
        owner_summary["remediation_owner"].nunique()
        if not owner_summary.empty and "remediation_owner" in owner_summary
        else 0
    ),
)
metric_cols[4].metric(
    "Open",
    (
        int((tracker.get("status") != "Remediated").sum())
        if not tracker.empty and "status" in tracker
        else 0
    ),
)

chart_cols = st.columns(3)
with chart_cols[0]:
    render_bar_chart(
        value_counts_frame(tracker, "status"),
        x="status",
        y="finding_count",
        title="Findings By Status",
    )
with chart_cols[1]:
    render_bar_chart(
        value_counts_frame(tracker, "sla_status"),
        x="sla_status",
        y="finding_count",
        title="Findings By SLA Status",
    )
with chart_cols[2]:
    render_bar_chart(
        value_counts_frame(tracker, "remediation_owner"),
        x="remediation_owner",
        y="finding_count",
        title="Findings By Owner",
    )

st.subheader("Overdue Findings")
st.dataframe(overdue, width="stretch")

st.subheader("Due-Soon Findings")
st.dataframe(due_soon, width="stretch")

st.subheader("Owner Workload Summary")
st.dataframe(owner_summary, width="stretch")

st.subheader("Remediation Summary")
st.dataframe(summary, width="stretch")

st.subheader("Remediation Tracker")
st.dataframe(tracker, width="stretch")
