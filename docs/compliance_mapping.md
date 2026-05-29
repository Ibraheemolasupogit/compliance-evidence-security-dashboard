# Compliance Mapping

Normalized findings are mapped offline using `data/reference/category_mapping.csv` and `data/reference/controls_reference.csv`.

The current MVP maps by finding category, preserves explicit mappings already present on a finding, and fills missing CIS, NIST, ISO-style, and control theme fields from the reference data. Findings that still have no CIS, NIST, or ISO-style mapping are exported to `outputs/unmapped_findings.csv` for follow-up.

Generated compliance outputs:

- `outputs/control_mapping_summary.csv`
- `outputs/control_coverage_summary.csv`
- `outputs/unmapped_findings.csv`
- `reports/compliance_evidence_pack.md`
