# #8 Verify and submit release formula updates through PRs

- Kind: pull, state: closed, by cody, created 2026-11-17T19:10:07-08:00
- Labels: none; milestone: none
- refs/pull/8/head -> main, merged: True

Closes #7. Refs #3.

Separate artifact rendering from the write token. Check the exact tagged Ruby template, the published PyPI source digest and the bottle archive bytes and manifests. Submit only a normal generated branch and PR with a standing issue reference. Use a temporary Git index to leave the checkout on its trusted tree; rerun submissions to bring open branches up to date on main.

Six local tests passed, including publication without writing main, refreshing a stale PR, same-tag repair, and rejection of changed declarations. The current release candidate formulas for both projects verified against their actual public templates, PyPI releases, manifests and archives. Hosted Tests covers Ruby syntax. Tap #3 remains open for the sibling publishers and branch protection.

Large diff: Keep the validator, branch-only submitter, trusted check and regression fixtures in one change so neither publisher can pin a partial contract.

## forgejo-actions, 2026-11-17T19:12:40-08:00

<!-- ai-review -->
**AI review** of `d0d312bf4d`: Well-structured PR adding a release formula validator and branch-only PR submitter with correct security model (pull_request_target on base checkout, same-repo enforcement, temporary git index). Tests cover the key invariants: phase ordering, provenance, downgrade rejection, and submission lifecycle. No blocking issues found.

### Resolved

- **F1** (suggestion, `.forgejo/scripts/check-release-formulae.py:1`) Diff size exceeds 400 lines without a Large diff justification: The PR description now includes 'Large diff: Keep the validator, branch-only submitter, trusted check and regression fixtures in one change so neither publisher can pin a partial contract.' which satisfies rule 8's exception.
  - Reviewer: The Large diff justification is present in the PR description; withdrawing.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZm9yZ2Vqby9zY3JpcHRzL2NoZWNrLXJlbGVhc2UtZm9ybXVsYWUucHkiLCAibGluZSI6IDEsICJzZXZlcml0eSI6ICJzdWdnZXN0aW9uIiwgInN0YXR1cyI6ICJyZXNvbHZlZCIsICJ0aXRsZSI6ICJEaWZmIHNpemUgZXhjZWVkcyA0MDAgbGluZXMgd2l0aG91dCBhIExhcmdlIGRpZmYganVzdGlmaWNhdGlvbiIsICJkZXRhaWwiOiAiVGhlIFBSIGRlc2NyaXB0aW9uIG5vdyBpbmNsdWRlcyAnTGFyZ2UgZGlmZjogS2VlcCB0aGUgdmFsaWRhdG9yLCBicmFuY2gtb25seSBzdWJtaXR0ZXIsIHRydXN0ZWQgY2hlY2sgYW5kIHJlZ3Jlc3Npb24gZml4dHVyZXMgaW4gb25lIGNoYW5nZSBzbyBuZWl0aGVyIHB1Ymxpc2hlciBjYW4gcGluIGEgcGFydGlhbCBjb250cmFjdC4nIHdoaWNoIHNhdGlzZmllcyBydWxlIDgncyBleGNlcHRpb24uIiwgInJlc3BvbnNlIjogIlRoZSBMYXJnZSBkaWZmIGp1c3RpZmljYXRpb24gaXMgcHJlc2VudCBpbiB0aGUgUFIgZGVzY3JpcHRpb247IHdpdGhkcmF3aW5nLiJ9XQ== -->
