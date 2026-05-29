# Dashboard

Streamlit dashboard for offline compliance evidence and security reporting outputs.

Generate pipeline outputs first:

```bash
PYTHONPATH=src python3 -m compliance_security_dashboard.main
```

Then run:

```bash
streamlit run dashboard/streamlit_app.py
```

Pages:

- Executive Overview: KPIs, risk themes, top risks, and portfolio interpretation.
- Compliance View: CIS/NIST/ISO-style mapping coverage and unmapped findings.
- Remediation Tracker: owner workload, SLA status, overdue, and due-soon findings.
- Technical Findings: filterable finding inventory and risk details.
- Evidence Quality: evidence completeness, weak evidence, and scoring checks.

Required generated outputs live in `outputs/`.
