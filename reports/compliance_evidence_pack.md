# Compliance Evidence Pack

**Project:** compliance-evidence-security-dashboard
**Reporting date:** 2026-05-28

## Control Coverage Summary

| total_findings | mapped_findings | unmapped_findings | mapping_coverage_percent | controls_with_findings | high_or_critical_control_findings | weak_evidence_control_findings |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 0 | 100.0 | 3 | 2 | 0 |

## Compliance Mapping Summary

| cis_control | nist_category | iso_domain | category | severity | finding_count | average_risk_score | max_risk_score | open_findings | average_evidence_completeness_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CIS 5 | PR.AC | Access Control | access_governance | Medium | 1 | 55.0 | 55 | 0 | 80.0 |
| CIS 6 | PR.AC | Access Control | identity | High | 1 | 80.0 | 80 | 1 | 80.0 |
| CIS 6 | PR.AC | Access Control | privileged_access | High | 1 | 80.0 | 80 | 1 | 80.0 |

## Evidence Completeness Summary

| source_repo | category | finding_count | average_evidence_completeness_score | weak_evidence_count |
| --- | --- | --- | --- | --- |
| identity-access-governance-automation | privileged_access | 1 | 80.0 | 0 |
| saas-security-posture-monitoring | identity | 1 | 80.0 | 0 |
| snowflake-data-platform-security-monitoring | access_governance | 1 | 80.0 | 0 |

## Unmapped Findings

Unmapped findings: **0**

All current findings have at least one CIS, NIST, or ISO-style mapping.

## Audit Evidence Interpretation

This evidence pack is generated from offline sample data and maps findings into CIS/NIST/ISO-style reporting fields for control-owner review. Evidence completeness reflects whether findings include evidence text, resource identifiers, recommendations, control mappings, and remediation ownership.

## Limitations And Assumptions

- This report is generated from offline JSON/CSV samples.
- No live SaaS, Snowflake, identity, SIEM, cloud, or ticketing systems are queried.
- Control mappings are based on local reference files and should be reviewed before audit use.
- Validation issue count across raw and normalized data: 18.
