"""Compliance view dashboard page."""

from __future__ import annotations

import streamlit as st
from dashboard.dashboard_utils import (
    first_record,
    format_percentage,
    load_csv_output,
    output_path,
    render_bar_chart,
    render_missing_output_warning,
    value_counts_frame,
)

st.set_page_config(page_title="Compliance View", layout="wide")
st.title("Compliance View")

required_outputs = [
    output_path("unified_findings.csv"),
    output_path("control_mapping_summary.csv"),
    output_path("control_coverage_summary.csv"),
    output_path("unmapped_findings.csv"),
]
render_missing_output_warning(required_outputs)

findings = load_csv_output(output_path("unified_findings.csv"))
mapping_summary = load_csv_output(output_path("control_mapping_summary.csv"))
coverage = first_record(load_csv_output(output_path("control_coverage_summary.csv")))
unmapped = load_csv_output(output_path("unmapped_findings.csv"))

metric_cols = st.columns(6)
metric_cols[0].metric("Total Findings", coverage.get("total_findings", len(findings)))
metric_cols[1].metric("Mapped", coverage.get("mapped_findings", 0))
metric_cols[2].metric("Unmapped", coverage.get("unmapped_findings", 0))
metric_cols[3].metric(
    "Coverage", format_percentage(coverage.get("mapping_coverage_percent", 0))
)
metric_cols[4].metric("Controls", coverage.get("controls_with_findings", 0))
metric_cols[5].metric(
    "High/Critical",
    coverage.get("high_or_critical_control_findings", 0),
)

chart_cols = st.columns(3)
with chart_cols[0]:
    render_bar_chart(
        value_counts_frame(findings, "cis_control"),
        x="cis_control",
        y="finding_count",
        title="Findings By CIS Control",
    )
with chart_cols[1]:
    render_bar_chart(
        value_counts_frame(findings, "nist_category"),
        x="nist_category",
        y="finding_count",
        title="Findings By NIST Category",
    )
with chart_cols[2]:
    render_bar_chart(
        value_counts_frame(findings, "iso_domain"),
        x="iso_domain",
        y="finding_count",
        title="Findings By ISO-Style Domain",
    )

st.subheader("Control Mapping Summary")
st.dataframe(mapping_summary, width="stretch")

st.subheader("Unmapped Findings")
if unmapped.empty:
    st.success("No unmapped findings in the current output set.")
else:
    st.dataframe(unmapped, width="stretch")

st.subheader("Compliance Interpretation")
st.write(
    "Compliance mapping links technical findings to CIS, NIST, and ISO-style "
    "control language. Unmapped findings should be reviewed and added to the "
    "offline category/control references before audit-facing use."
)
