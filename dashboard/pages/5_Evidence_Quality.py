"""Evidence quality dashboard page."""

from __future__ import annotations

import streamlit as st
from dashboard.dashboard_utils import (
    format_percentage,
    load_csv_output,
    output_path,
    render_missing_output_warning,
)

st.set_page_config(page_title="Evidence Quality", layout="wide")
st.title("Evidence Quality")

required_outputs = [
    output_path("unified_findings.csv"),
    output_path("evidence_quality_summary.csv"),
]
render_missing_output_warning(required_outputs)

findings = load_csv_output(output_path("unified_findings.csv"))
summary = load_csv_output(output_path("evidence_quality_summary.csv"))

average_evidence = (
    findings["evidence_completeness_score"].mean()
    if not findings.empty and "evidence_completeness_score" in findings
    else 0
)
weak_evidence = (
    findings[findings["evidence_completeness_score"] < 60]
    if not findings.empty and "evidence_completeness_score" in findings
    else findings
)

metric_cols = st.columns(3)
metric_cols[0].metric(
    "Avg Evidence Completeness",
    format_percentage(average_evidence),
)
metric_cols[1].metric("Weak Evidence Findings", len(weak_evidence))
metric_cols[2].metric("Evidence Groups", len(summary))

st.subheader("Evidence Completeness Distribution")
if findings.empty or "evidence_completeness_score" not in findings:
    st.info("No evidence completeness data available.")
else:
    distribution = findings["evidence_completeness_score"].value_counts().sort_index()
    st.bar_chart(
        distribution,
        x_label="Evidence completeness score",
        y_label="Finding count",
    )

st.subheader("Evidence Quality Summary")
st.dataframe(summary, width="stretch")

st.subheader("Weak Evidence Findings")
if weak_evidence.empty:
    st.success("No findings below the weak evidence threshold.")
else:
    st.dataframe(
        weak_evidence[
            [
                "finding_id",
                "title",
                "source_repo",
                "category",
                "severity",
                "evidence_completeness_score",
                "remediation_owner",
            ]
        ],
        width="stretch",
    )

st.subheader("Evidence Scoring Checks")
st.markdown(
    "- Evidence text is present.\n"
    "- Resource identifier is present.\n"
    "- Recommendation is present.\n"
    "- Control mapping is present.\n"
    "- Remediation owner is present."
)
