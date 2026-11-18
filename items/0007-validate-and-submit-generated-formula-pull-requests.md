# #7 Validate and submit generated formula pull requests

- Kind: issue, state: closed, by cody, created 2026-11-17T18:48:46-08:00
- Labels: status:in-progress, type:chore; milestone: none

First step of #3. Add the trusted validation for generated release formula and bottles PRs, with package and manifest provenance and monotonically advancing versions. Provide a narrow branch-only PR submitter so the sibling release jobs can switch without a direct main push. Prove the gate and submitter with fixtures before rewiring native publishers.
