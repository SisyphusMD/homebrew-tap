# #37 ci: map PROJECT_RULES_TOKEN into the shared jobs

- Kind: pull, state: closed, by cody, created 2026-11-26T21:11:13-08:00
- Labels: none; milestone: none
- refs/pull/37/head -> main, merged: True

Refs SisyphusMD/project-rules#143

Trigger: the shared Lint, Secrets and AI review jobs are about to read the owner's private `.project-rules` manifest with the owner's read-only Actions secret `PROJECT_RULES_TOKEN`, and a called workflow sees only the secrets its caller maps in. This maps it, as the canonical callers in SisyphusMD/project-rules do. Until SisyphusMD/project-rules#140 merges the jobs ignore it, so nothing changes yet.

No tests: caller wiring only; the next PR after SisyphusMD/project-rules#140 merges proves it, since its Lint, Secrets and AI review checks read the manifest with this token.


## forgejo-actions, 2026-11-26T21:16:09-08:00

<!-- ai-review -->
**AI review** of `b431eec29c`: Clean, minimal wiring PR that maps PROJECT_RULES_TOKEN into the shared-lint and shared-review called jobs, exactly as step 2 of project-rules#143 requires. No correctness, security, or scope issues found.

No findings.

Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W10= -->
