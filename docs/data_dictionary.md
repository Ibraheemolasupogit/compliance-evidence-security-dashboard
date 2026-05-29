# Data Dictionary

## Unified Finding Fields

- `finding_id`: stable finding identifier.
- `source_system`: source domain such as `saas`, `snowflake`, or `iam`.
- `source_repo`: upstream portfolio project represented by the finding.
- `title`: short finding name.
- `description`: optional detail.
- `resource_type`, `resource_name`, `resource_id`: affected asset fields.
- `category`: finding category used for mapping and grouping.
- `severity`: standardized as `Critical`, `High`, `Medium`, `Low`, or `Info`.
- `risk_score`: integer risk score from 0 to 100.
- `control_mapping`: internal control identifier.
- `cis_control`, `nist_category`, `iso_domain`: compliance reporting fields.
- `evidence`: supporting evidence text.
- `recommendation`: remediation guidance.
- `remediation_owner`: accountable team or owner.
- `status`: standardized remediation status.
- `created_at`, `updated_at`, `due_date`: lifecycle dates.
- `sla_status`: `Closed`, `Overdue`, `Due Soon`, `Within SLA`, or `No Due Date`.
- `evidence_completeness_score`: percentage score from 0 to 100.

## Reference Data

- `data/reference/category_mapping.csv`: maps source categories to control metadata.
- `data/reference/controls_reference.csv`: control catalog and evidence expectations.
- `data/reference/owners_reference.csv`: example owner metadata.
