# Technical Report

**Project:** compliance-evidence-security-dashboard
**Reporting date:** 2026-05-29

## Severity, Category, And Source Breakdown

| source_repo | severity | category | finding_count | average_risk_score | max_risk_score |
| --- | --- | --- | --- | --- | --- |
| identity-access-governance-automation | High | privileged_access | 1 | 80.0 | 80 |
| saas-security-posture-monitoring | High | identity | 1 | 80.0 | 80 |
| snowflake-data-platform-security-monitoring | Medium | access_governance | 1 | 55.0 | 55 |

## Findings Table

| finding_id | source_system | source_repo | title | description | resource_type | resource_name | resource_id | category | severity | risk_score | control_mapping | cis_control | nist_category | iso_domain | evidence | recommendation | remediation_owner | status | created_at | updated_at | due_date | sla_status | evidence_completeness_score | control_theme | is_mapped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAAS-001 | saas | saas-security-posture-monitoring | MFA not enforced for admin users |  |  |  |  | identity | High | 80 | CTRL-IAM-001 | CIS 6 | PR.AC | Access Control | Offline sample finding | Review finding and apply documented remediation. | SaaS Platform Team | Open | 2026-05-01 | 2026-05-01 | 2026-05-15 | Overdue | 80 | Identity and Access Management | True |
| IAM-001 | iam | identity-access-governance-automation | Dormant privileged account requires review |  |  |  |  | privileged_access | High | 80 | CTRL-IAM-002 | CIS 6 | PR.AC | Access Control | Offline sample finding | Review finding and apply documented remediation. | Identity Governance Team | Open | 2026-05-05 | 2026-05-05 | 2026-05-19 | Overdue | 80 | Privileged Access Management | True |
| SNOW-001 | snowflake | snowflake-data-platform-security-monitoring | Privileged role assigned to inactive user |  |  |  |  | access_governance | Medium | 55 | CTRL-DATA-002 | CIS 5 | PR.AC | Access Control | Offline sample finding | Review finding and apply documented remediation. | Data Platform Team | In Progress | 2026-05-03 | 2026-05-03 | 2026-06-02 | Due Soon | 80 | Data Platform Access Governance | True |

## Top Technical Risks

### SAAS-001 - MFA not enforced for admin users

- Source repo: saas-security-posture-monitoring
- Source system: saas
- Category: identity
- Severity: High
- Risk score: 80
- Resource:  / 
- Status: Open
- Owner: SaaS Platform Team
- Recommendation: Review finding and apply documented remediation.
### IAM-001 - Dormant privileged account requires review

- Source repo: identity-access-governance-automation
- Source system: iam
- Category: privileged_access
- Severity: High
- Risk score: 80
- Resource:  / 
- Status: Open
- Owner: Identity Governance Team
- Recommendation: Review finding and apply documented remediation.
### SNOW-001 - Privileged role assigned to inactive user

- Source repo: snowflake-data-platform-security-monitoring
- Source system: snowflake
- Category: access_governance
- Severity: Medium
- Risk score: 55
- Resource:  / 
- Status: In Progress
- Owner: Data Platform Team
- Recommendation: Review finding and apply documented remediation.
