# Architecture

This project is an offline reporting and evidence layer for security findings from SaaS, Snowflake/data platform, and identity/access governance monitoring projects.

```text
data/input/*.json
      ↓
ingestion/source_router.py
      ↓
normalization/schema_normalizer.py
      ↓
validation/finding_validator.py
      ↓
scoring/risk_scorer.py + evidence_scorer.py
      ↓
compliance/control_mapper.py + coverage_analyzer.py
      ↓
remediation/remediation_tracker.py + sla_calculator.py
      ↓
outputs/*.csv + outputs/*.json
      ↓
reporting/templates/*.j2 → reports/*.md
      ↓
dashboard/*.py → Streamlit pages
```

## Design Notes

- The pipeline is deterministic and runs from local files only.
- Reference data lives in `data/reference/`.
- Configuration lives in `config/`.
- Generated data products live in `outputs/`.
- Generated stakeholder reports live in `reports/`.
- The dashboard reads generated outputs rather than calling external systems.

No live SaaS, cloud, Snowflake, SIEM, or identity provider connections are used.
