# #23 chore(ci): bring the AI review copy up to canonical project-rules 0e929cc

- Kind: issue, state: closed, by cody, created 2026-11-21T18:21:46-08:00
- Labels: status:in-progress, type:chore; milestone: none

Copy `.forgejo/scripts/ai-review.py` and `.forgejo/workflows/ai-review.yml` from SisyphusMD/project-rules 0e929cc (this repo's copies are on 9369e1a). The script gains the connect retry (#109), the malformed-answer re-ask with a strict schema (#110, #114) and the bounded replies (#58). The workflow pins the checkout to the base commit and sets `BOT_LOGIN`. Part of SisyphusMD/project-rules#113.

## cody, 2026-11-21T20:30:37-08:00

Merged via #24 at e880328: ai-review.py and ai-review.yml are byte-for-byte canonical project-rules 64b857c.
