# Remediation Model

The remediation model tracks ownership, lifecycle status, due dates, and SLA status for each unified finding.

Supported SLA statuses are `Closed`, `Overdue`, `Due Soon`, `Within SLA`, and `No Due Date`. Findings marked `Remediated` or `False Positive` are treated as closed. Open findings with due dates before the current date are overdue; open findings due within the next seven days are due soon.

The pipeline exports a remediation tracker, grouped remediation summaries, owner workload summaries, and separate overdue/due-soon finding lists.
