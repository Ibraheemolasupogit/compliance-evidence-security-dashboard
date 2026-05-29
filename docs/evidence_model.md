# Evidence Model

Evidence quality is scored from offline finding fields including evidence text, resource identifiers, recommendations, control mappings, and remediation ownership.

The compliance evidence pack is generated as Markdown in `reports/compliance_evidence_pack.md` and summarizes mapping coverage, evidence completeness, unmapped findings, and audit-readiness assumptions.

Evidence completeness checks:

- evidence text
- resource identifier
- recommendation
- control mapping
- remediation owner

Each present check contributes equally to a 0-100 score.
