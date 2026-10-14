Review the completed experiment in /workspace.

Read TASK.md, PLAN.md, algorithms.py, results.csv, REPORT.md,
and PROGRESS.md.

Independently audit:
- Compliance with the original task.
- Correctness of the implementations and measurement procedure.
- Numerical claims, recalculated from results.csv.
- Whether the conclusions are supported by the evidence.
- Reproducibility and recovery after interruption.

Write /workspace/AUDIT.md containing:
1. Checks performed and their results.
2. Each issue found, with specific evidence.
3. Corrected calculations where applicable.
4. What remains uncertain or cannot be verified.
5. Suggested fixes, without applying them.

Do not modify existing files, including PROGRESS.md.
Do not rerun algorithms.py or regenerate the benchmark.
You may execute separate analysis code to inspect the existing CSV.
Write any supporting analysis files under /workspace/audit_work/.
If a claim is correct, say so. Do not invent problems.
Finish when AUDIT.md is complete.

Execution guidance:
- Inspect any existing AUDIT.md and audit_work files before continuing.
- Parse results.csv using Python. Print compact summaries and exceptions;
  do not print the full CSV into the conversation.
- Save audit findings incrementally to AUDIT.md.
- Preserve the original experiment files.
