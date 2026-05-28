"""Streamlit dashboard placeholder for offline sample outputs."""

from pathlib import Path

import pandas as pd
import streamlit as st

SAMPLE_FINDINGS = Path("outputs/sample/unified_findings.csv")

st.set_page_config(page_title="Compliance Evidence Dashboard", layout="wide")
st.title("Compliance Evidence Security Dashboard")
st.caption("Offline-first dashboard placeholder using sample output files.")

if SAMPLE_FINDINGS.exists():
    findings = pd.read_csv(SAMPLE_FINDINGS)
    col1, col2, col3 = st.columns(3)
    col1.metric("Findings", len(findings))
    col2.metric("Open", int((findings["status"] == "open").sum()))
    col3.metric("Sources", findings["source_system"].nunique())
    st.dataframe(findings, use_container_width=True)
else:
    st.info("Sample findings CSV not found. Generate outputs before using this view.")
