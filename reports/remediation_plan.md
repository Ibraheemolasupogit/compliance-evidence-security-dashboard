# Remediation Plan

**Project:** compliance-evidence-security-dashboard
**Reporting date:** 2026-05-28

## SLA Status Explanation

`Closed` findings are remediated or false positive. `Overdue` findings are past due and still open. `Due Soon` findings are due within seven days. `Within SLA` findings have more than seven days remaining. `No Due Date` findings need remediation planning.

## Owner Workload Summary

| remediation_owner | total_findings | open_findings | overdue_findings | due_soon_findings | high_or_critical_findings | average_risk_score | average_evidence_completeness_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Data Platform Team | 1 | 1 | 0 | 1 | 0 | 55.0 | 80.0 |
| Identity Governance Team | 1 | 1 | 1 | 0 | 1 | 80.0 | 80.0 |
| SaaS Platform Team | 1 | 1 | 1 | 0 | 1 | 80.0 | 80.0 |

## Overdue Findings

| finding_id | title | severity | risk_score | source_repo | source_system | category | cis_control | nist_category | iso_domain | remediation_owner | status | due_date | sla_status | recommendation | evidence_completeness_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAAS-001 | MFA not enforced for admin users | High | 80 | saas-security-posture-monitoring | saas | identity | CIS 6 | PR.AC | Access Control | SaaS Platform Team | Open | 2026-05-15 | Overdue | Review finding and apply documented remediation. | 80 |
| IAM-001 | Dormant privileged account requires review | High | 80 | identity-access-governance-automation | iam | privileged_access | CIS 6 | PR.AC | Access Control | Identity Governance Team | Open | 2026-05-19 | Overdue | Review finding and apply documented remediation. | 80 |

## Due-Soon Findings

| finding_id | title | severity | risk_score | source_repo | source_system | category | cis_control | nist_category | iso_domain | remediation_owner | status | due_date | sla_status | recommendation | evidence_completeness_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SNOW-001 | Privileged role assigned to inactive user | Medium | 55 | snowflake-data-platform-security-monitoring | snowflake | access_governance | CIS 5 | PR.AC | Access Control | Data Platform Team | In Progress | 2026-06-02 | Due Soon | Review finding and apply documented remediation. | 80 |

## Recommended Prioritisation

1. Critical overdue findings
2. High overdue findings
3. Critical due-soon findings
4. High due-soon findings
5. Weak-evidence findings
6. Remaining open findings

## High And Critical Findings

- **SAAS-001:** MFA not enforced for admin users - Overdue - owner: SaaS Platform Team
- **IAM-001:** Dormant privileged account requires review - Overdue - owner: Identity Governance Team
