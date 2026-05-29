"""Technical findings dashboard page."""

from __future__ import annotations

import streamlit as st
from dashboard.dashboard_utils import (
    apply_sidebar_filters,
    load_csv_output,
    output_path,
    render_missing_output_warning,
)

st.set_page_config(page_title="Technical Findings", layout="wide")
st.title("Technical Findings")

required_outputs = [output_path("unified_findings.csv")]
render_missing_output_warning(required_outputs)

findings = load_csv_output(output_path("unified_findings.csv"))

filtered = apply_sidebar_filters(
    findings,
    filter_columns=[
        "severity",
        "source_repo",
        "category",
        "remediation_owner",
        "status",
        "sla_status",
    ],
    search_columns=["finding_id", "title", "resource_name"],
)

st.metric("Displayed Findings", len(filtered))

columns = [
    "finding_id",
    "title",
    "severity",
    "risk_score",
    "source_repo",
    "source_system",
    "category",
    "resource_type",
    "resource_name",
    "status",
    "sla_status",
    "remediation_owner",
    "recommendation",
]
available_columns = [column for column in columns if column in filtered.columns]

st.subheader("Technical Findings Table")
st.dataframe(
    filtered[available_columns] if available_columns else filtered,
    width="stretch",
)

st.subheader("Top Technical Risks")
if filtered.empty:
    st.info("No findings match the current filters.")
else:
    top_risks = filtered.sort_values("risk_score", ascending=False).head(10)
    st.dataframe(top_risks[available_columns], width="stretch")

    st.subheader("Finding Details")
    for finding in top_risks.to_dict(orient="records"):
        with st.expander(f"{finding.get('finding_id')} - {finding.get('title')}"):
            detail_cols = st.columns(3)
            detail_cols[0].metric("Severity", finding.get("severity", ""))
            detail_cols[1].metric("Risk Score", finding.get("risk_score", 0))
            detail_cols[2].metric("SLA", finding.get("sla_status", ""))
            st.write(
                f"**Source:** {finding.get('source_repo')} / "
                f"{finding.get('source_system')}"
            )
            st.write(f"**Category:** {finding.get('category')}")
            st.write(f"**Owner:** {finding.get('remediation_owner')}")
            st.write(f"**Recommendation:** {finding.get('recommendation')}")
