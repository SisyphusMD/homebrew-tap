# #30 chore(lint): lint this repo's own scripts

- Kind: pull, state: closed, by cody, created 2026-11-24T18:05:48-08:00
- Labels: none; milestone: none
- refs/pull/30/head -> main, merged: True

Closes #29

`ruff.toml` excluded all of `.forgejo/scripts`, which hid this repo's two scripts from Lint once the gate script copies left (#27). Only `issue-archive.py`, still a copy, is excluded now; `ruff check .` covers both scripts and passes.

This description first had no issue, so that the fetched `Issue link` had to fail; that run is the failing proof for #27.

## forgejo-actions, 2026-11-24T18:11:02-08:00

<!-- ai-review -->
**AI review** of `bdf16d58e7`: The PR narrows the ruff exclusion from the entire `.forgejo/scripts` directory to just `issue-archive.py`, correctly bringing the repo's own scripts under linting as described in issue #29. The earlier finding about a missing issue link is resolved.

### Resolved

- **F1** (blocking, `ruff.toml:1`) No linked issue (rules 1 and 6): The PR description now includes `Closes #29` and issue #29 exists with a matching description. Rules 1 and 6 are satisfied.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICJydWZmLnRvbWwiLCAibGluZSI6IDEsICJzZXZlcml0eSI6ICJibG9ja2luZyIsICJzdGF0dXMiOiAicmVzb2x2ZWQiLCAidGl0bGUiOiAiTm8gbGlua2VkIGlzc3VlIChydWxlcyAxIGFuZCA2KSIsICJkZXRhaWwiOiAiVGhlIFBSIGRlc2NyaXB0aW9uIG5vdyBpbmNsdWRlcyBgQ2xvc2VzICMyOWAgYW5kIGlzc3VlICMyOSBleGlzdHMgd2l0aCBhIG1hdGNoaW5nIGRlc2NyaXB0aW9uLiBSdWxlcyAxIGFuZCA2IGFyZSBzYXRpc2ZpZWQuIiwgInJlc3BvbnNlIjogIiJ9XQ== -->
