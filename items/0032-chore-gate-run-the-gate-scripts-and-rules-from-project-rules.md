# #32 chore(gate): run the gate scripts and rules from project-rules main

- Kind: pull, state: closed, by cody, created 2026-11-24T19:11:26-08:00
- Labels: none; milestone: none
- refs/pull/32/head -> main, merged: True

Closes #31

This repo ran its own copies of the gate scripts and kept a copy of the rules for the AI review, and copies drift. `ci.yml` and `ai-review.yml` now fetch the scripts and `RULES.md` from project-rules main on every run and fail when they cannot (SisyphusMD/project-rules#78). The gate jobs and `ai-review.yml` are project-rules main's (6a6d41b4), and the copies are removed in the same change, so no run is left without either.

The scripts moved in #27; this drops the rules copy and re-copies the two workflows, whose comments changed.

Large diff: 129 of the removed lines are the deleted copies, and the added workflow lines come from project-rules main, where they were reviewed and tested.


## forgejo-actions, 2026-11-24T19:11:46-08:00

<!-- ai-review -->
**AI review** of `61d76533fb`: PR removes the now-unused local RULES.md copy and corrects comments in ci.yml and ai-review.yml to reflect that the checkout step reads CONTRIBUTING.md rather than RULES.md. All changes are comment-only or a file deletion, directly serving issue #31, with no functional code changes.

No findings.

Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W10= -->
