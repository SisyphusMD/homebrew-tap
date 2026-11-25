# #29 Lint this repo's own scripts

- Kind: issue, state: closed, by cody, created 2026-11-24T18:02:10-08:00
- Labels: status:in-progress, type:chore; milestone: none

`ruff.toml` excludes all of `.forgejo/scripts` because the gate script copies follow project-rules' ruff settings. Those copies are gone (#27), so the exclusion now only hides this repo's own `check-release-formulae.py` and `open-release-formula-pr.py`. Exclude only `issue-archive.py`, which is still a copy.

## cody, 2026-11-24T18:24:07-08:00

Landed in #30 (b2ac20f3).
