# #20 AI review: 40-minute deadline inside a 45-minute job

- Kind: pull, state: closed, by cody, created 2026-11-19T17:41:23-08:00
- Labels: none; milestone: none
- refs/pull/20/head -> main, merged: True

Closes #19

Sync from SisyphusMD/project-rules#108 (byte-identical copies of the script and workflow; tests live there). A 40-minute deadline from the review's start ends a slow review with an error status instead of the job being killed at 20 minutes with the required check left pending. The job limit is now 45 minutes.

## forgejo-actions, 2026-11-19T17:48:11-08:00

<!-- ai-review -->
**AI review** of `691dc4c64d`: Clean sync of the AI review script and workflow from project-rules#108: a 40-minute SIGALRM deadline inside a 45-minute job replaces the old 20-minute hard kill, and the exception handling is restructured so every failure path sets an error status instead of leaving the required check pending. The signal/alarm usage, exception hierarchy, and try/finally ordering are all correct for a single-threaded CI script.

No findings.

Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W10= -->
