# #27 Run the gate scripts from project-rules main

- Kind: issue, state: closed, by cody, created 2026-11-24T17:52:02-08:00
- Labels: status:in-progress, type:chore; milestone: none

Cody decided on SisyphusMD/project-rules#78 (2026-11-24) that every repo runs the gate scripts from project-rules main instead of its own copy. Switch `ci.yml` and `ai-review.yml` to canonical, remove the four gate script copies, and copy `mirror-lockdown.yml` again for its source header. This is the pilot. issue-archive.py stays a copy.

## cody, 2026-11-24T18:00:34-08:00

Scope: `.forgejo/RULES.md` is synced to project-rules main (26da87ec) in the same PR. Rule 15 there changed with the shared scripts, the reviewer reads this copy, and rule 22 has it as a synced copy of the whole file, so it is copied verbatim rather than in parts.

## cody, 2026-11-24T18:24:07-08:00

Landed in #28 (27caff80). Proof on #30 (head bdf16d58): `Issue link` fetched project-rules 26da87ec and failed on the missing issue, then every required check passed with it named.
