# #36 docs(gate): match the canonical caller headers

- Kind: pull, state: closed, by cody, created 2026-11-25T22:18:49-08:00
- Labels: none; milestone: none
- refs/pull/36/head -> main, merged: True

Refs SisyphusMD/project-rules#78

The pilot callers here predate two header fixes in project-rules: a bare `(#78)` pointed at this repo's issue #78, and line 1 now says protection requires every called job. Both files are now byte-equal to project-rules main's callers.

No tests: header comments only.

## forgejo-actions, 2026-11-25T22:19:01-08:00

<!-- ai-review -->
**AI review** of `b08b2834f5`: Comment-only header corrections in two workflow files to match the canonical project-rules versions: fixes the ambiguous bare `(#78)` to `SisyphusMD/project-rules#78` and aligns wording. No behavior changes, no tests needed.

No findings.

Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W10= -->
