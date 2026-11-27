# #39 chore(ci): call the shared issue-archive workflow

- Kind: pull, state: closed, by cody, created 2026-11-27T07:01:30-08:00
- Labels: none; milestone: none
- chore/38-shared-archive -> main, merged: True

Replaces the copied issue-archive job with the caller from project-rules main and deletes the copied script, which no longer runs.

Closes #38


## forgejo-actions, 2026-11-27T07:03:59-08:00

<!-- ai-review -->
**AI review** of `db8881c401`: Clean, focused change that replaces the locally-copied issue-archive job and script with a call to the shared workflow in project-rules, exactly as issue #38 requests. The diff is small, the concurrency group and schedule are preserved, and the only secret passed (PROJECT_RULES_TOKEN) is scoped and explained.

No findings.

Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W10= -->
