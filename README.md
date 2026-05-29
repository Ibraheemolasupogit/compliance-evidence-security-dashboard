# Compliance Evidence Security Dashboard

Offline compliance evidence, remediation, risk reporting, and dashboarding layer for SaaS, Snowflake/data platform, and identity/access governance security findings.

## Problem Statement

Security monitoring creates value only when raw findings become clear risk decisions, control evidence, remediation ownership, and stakeholder-ready reporting. This project demonstrates that final reporting layer: it aggregates findings from security monitoring projects, normalises them, scores risk and evidence quality, maps them to controls, tracks remediation SLAs, generates Markdown reports, and presents the results in a Streamlit dashboard.

## Why This Matters

Data Security Engineer and security reporting roles often sit between technical control monitoring, GRC requirements, remediation delivery, and executive communication. This repo shows how to turn offline security findings into:

- compliance evidence and control coverage summaries
- risk-ranked remediation work
- overdue and due-soon tracking
- executive and technical reports
- dashboard views for multiple audiences

## Portfolio Architecture

This is repo 4 in a 5-repo security engineering portfolio.

- **SaaS Security Posture Monitor:** produces SaaS configuration and posture findings.
- **Snowflake Data Security Monitor:** produces data platform access and configuration findings.
- **Identity & Access Governance Automation:** produces privileged access and lifecycle findings.
- **Compliance Evidence Security Dashboard:** aggregates those findings into evidence, remediation, reports, and dashboards.

```text
Offline source findings
  ├─ SaaS findings JSON
  ├─ Snowflake findings JSON
  └─ IAM findings JSON
        ↓
ingestion → normalisation → validation → risk scoring
        ↓
compliance mapping → evidence scoring → remediation tracking
        ↓
CSV/JSON outputs → Markdown reports → Streamlit dashboard
```

## Capabilities

- Loads offline JSON findings from SaaS, Snowflake, and IAM sample sources.
- Normalises records into a unified finding schema.
- Validates required fields, severity, status, risk score bounds, and due dates.
- Standardises severity and remediation status values.
- Scores risk and evidence completeness.
- Maps findings to CIS/NIST/ISO-style control fields using offline reference CSVs.
- Calculates SLA status, overdue findings, due-soon findings, and owner workload.
- Exports CSV/JSON datasets for reporting and BI-style consumption.
- Generates Markdown reports for executives, engineers, remediation owners, and GRC.
- Provides a multi-page Streamlit dashboard backed by generated offline outputs.

## Generated Outputs

Pipeline outputs are written to `outputs/`:

- `unified_findings.json`
- `unified_findings.csv`
- `risk_score_summary.csv`
- `evidence_quality_summary.csv`
- `control_mapping_summary.csv`
- `control_coverage_summary.csv`
- `unmapped_findings.csv`
- `remediation_tracker.csv`
- `remediation_summary.csv`
- `remediation_owner_summary.csv`
- `overdue_findings.csv`
- `due_soon_findings.csv`
- `validation_summary.json`

## Generated Reports

Markdown reports are written to `reports/`:

- `executive_summary.md`
- `technical_report.md`
- `remediation_plan.md`
- `compliance_evidence_pack.md`

## Dashboard Pages

The Streamlit dashboard includes:

- Executive Overview
- Compliance View
- Remediation Tracker
- Technical Findings
- Evidence Quality

## Tech Stack

- Python 3.11+
- pandas and pydantic
- PyYAML
- Jinja2
- Streamlit and Plotly
- pytest
- ruff and black
- GitHub Actions

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Run The Pipeline

```bash
PYTHONPATH=src python3 -m compliance_security_dashboard.main
```

Or:

```bash
./scripts/run_pipeline.sh
```

## Run Tests And Checks

```bash
python3 -m pytest
python3 -m ruff check .
python3 -m black --check .
python3 -m compileall src dashboard scripts
```

## Run The Dashboard

Generate outputs first, then run:

```bash
python3 -m streamlit run dashboard/streamlit_app.py
```

## Example Use Cases

- Show executives the top risks, open findings, and overdue remediation work.
- Give platform teams a filtered technical findings view.
- Give GRC and audit teams a control evidence pack with mapping coverage.
- Track remediation ownership, SLA status, and due-soon findings.
- Demonstrate risk reporting across SaaS, data platform, and IAM domains.

## Limitations

- Offline sample project only; no live integrations are included.
- No Microsoft Graph, Snowflake, Sentinel, Azure, SaaS, ticketing, or cloud credentials are required.
- Control mappings are simplified CIS/NIST/ISO-style examples, not official audit advice.
- Sample data is intentionally small so the project remains reviewable.

## Future Enhancements

- Add richer source-specific sample findings.
- Add Power BI-ready exports and schema documentation.
- Add dashboard screenshots for portfolio presentation.
- Add optional ticketing export stubs for remediation workflows.
- Expand controls into a fuller CIS/NIST/ISO reference model.

## Portfolio Value

This repo demonstrates skills relevant to Data Security Engineer, SaaS Security, Data Platform Security, GRC automation, and risk reporting roles:

- security data modelling
- evidence generation
- compliance mapping
- risk aggregation
- remediation tracking
- stakeholder reporting
- dashboarding
- offline-first, testable security engineering
