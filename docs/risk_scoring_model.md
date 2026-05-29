# Risk Scoring Model

Risk scores are currently derived from standardized severity when an explicit score is missing. The default scores are Critical 95, High 80, Medium 55, Low 25, and Info 5.

Remediation summaries use risk score and severity to highlight high-priority owner workload, especially high and critical findings that remain open, overdue, or due soon.

Generated risk outputs:

- `outputs/risk_score_summary.csv`
- portfolio risk metrics inside `outputs/validation_summary.json`
