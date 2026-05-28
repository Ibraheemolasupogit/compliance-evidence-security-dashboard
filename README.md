# Compliance Evidence Security Dashboard

Portfolio repository 4 of 5: a reporting, compliance evidence, remediation, and dashboarding layer for security findings from SaaS, Snowflake/data platform, and identity/access governance monitoring projects.

## What This Project Does

This project is designed to aggregate security findings from prior monitoring systems, normalize them into a common schema, score risk, map findings to compliance controls, track remediation status, and produce stakeholder-ready reports and dashboards.

The first version is intentionally offline-first. It uses sample JSON and CSV files only. There are no live API integrations, cloud dependencies, credentials, or external system calls.

## Why It Matters

Security monitoring only creates value when findings become evidence, decisions, and remediation. Compliance evidence and reporting help teams:

- Demonstrate control coverage for CIS, NIST-style, and internal security baselines.
- Communicate risk clearly to technical and non-technical stakeholders.
- Track ownership, SLAs, remediation progress, and evidence quality.
- Convert raw detections into executive summaries, technical reports, and audit-ready evidence packs.

## Portfolio Context

This repo follows the first three repositories in the portfolio:

- Repo 1: SaaS security posture monitoring.
- Repo 2: Snowflake and data platform security monitoring.
- Repo 3: Identity and access governance automation.
- Repo 4: Compliance evidence, reporting, remediation, and dashboarding.

Together, these projects demonstrate a security engineering workflow from continuous control monitoring through risk aggregation and executive communication.

## Offline-First MVP

The initial foundation runs from local sample files:

- `data/input/*.json` for offline source findings.
- `data/sample/*.json` and `data/sample/*.csv` for example normalized data.
- `data/reference/*.csv` for control, owner, and category mappings.
- `outputs/sample/*` for expected generated datasets.
- `reports/sample/*` for example report artifacts.

No Microsoft Graph, Snowflake, Sentinel, Azure, SaaS, or cloud credentials are required.

## Planned Pipeline

```text
ingestion -> normalisation -> validation -> risk scoring -> compliance mapping -> remediation tracking -> reports/dashboard
```

Expected outputs include:

- Unified findings JSON and CSV.
- Control mapping summaries.
- Control coverage summaries.
- Unmapped findings exports.
- Risk score summaries.
- Remediation tracker exports.
- Remediation owner workload and SLA status summaries.
- Overdue and due-soon finding exports.
- Executive summaries.
- Technical reports.
- Compliance evidence packs.
- Generated Markdown reports for executive, technical, remediation, and compliance audiences.
- Streamlit dashboard views.

## Tech Stack

- Python 3.11+
- pandas
- pydantic
- PyYAML
- Jinja2
- python-dateutil
- Streamlit
- Plotly
- pytest
- ruff
- black
- GitHub Actions

## Run Locally

The full pipeline will be implemented in later tasks. Once implementation begins, the intended local workflow is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compliance_security_dashboard.main
streamlit run dashboard/streamlit_app.py
pytest
```

For now, the dashboard placeholder can read `outputs/sample/unified_findings.csv`.

## Portfolio Value

This repository is built to show skills relevant to Data Security Engineer, SaaS Security Engineer, Data Platform Security, GRC automation, and risk reporting roles:

- Translating raw findings into normalized security evidence.
- Mapping security observations to controls and compliance themes.
- Prioritizing risk across SaaS, data platform, and IAM domains.
- Tracking remediation ownership and SLA status.
- Communicating clearly through dashboards and reports.
- Designing offline, testable foundations before adding integrations.

## Current Status

Initial production-style project foundation only. Live integrations, full pipeline logic, and advanced dashboarding are intentionally out of scope for this first version.
