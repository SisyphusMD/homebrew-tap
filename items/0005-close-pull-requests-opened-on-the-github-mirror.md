# #5 Close pull requests opened on the GitHub mirror

- Kind: pull, state: closed, by cody, created 2026-11-17T14:37:55-08:00
- Labels: none; milestone: none
- refs/pull/5/head -> main, merged: True

Closes #4

Copy the project-rules workflow that redirects new GitHub pull requests to Forgejo. The GitHub mirror will enable only the pinned lockdown action after the workflow is mirrored.

Validated the canonical file with actionlint and yamllint.

## forgejo-actions, 2026-11-17T14:39:17-08:00

<!-- ai-review -->
**AI review** of `846460fbff`: The mirror-lockdown workflow is well-structured: pinned action, minimal permissions, correct `if` guard against Forgejo/forks, and a helpful PR comment. One concern about the exclusion date potentially disabling the workflow.

### Open

- **F1** (suggestion, `.github/workflows/mirror-lockdown.yml:26`) exclude-pr-created-before may be in the future, disabling the workflow: `exclude-pr-created-before: "2026-11-17T00:00:00Z"` excludes every PR created before that timestamp. If the workflow is merged and activated before 2026-11-17, all PRs—including ones opened the same day—were created before the cutoff, so neither the `pull_request_target` trigger nor the schedule sweep would close anything. The workflow would be a no-op until that date. If 2026-11-17 is the intended go-live date, consider adding a comment saying so; otherwise set the value to the date the lockdown is actually enabled on the mirror so that new PRs are closed immediately.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZ2l0aHViL3dvcmtmbG93cy9taXJyb3ItbG9ja2Rvd24ueW1sIiwgImxpbmUiOiAyNiwgInNldmVyaXR5IjogInN1Z2dlc3Rpb24iLCAic3RhdHVzIjogIm9wZW4iLCAidGl0bGUiOiAiZXhjbHVkZS1wci1jcmVhdGVkLWJlZm9yZSBtYXkgYmUgaW4gdGhlIGZ1dHVyZSwgZGlzYWJsaW5nIHRoZSB3b3JrZmxvdyIsICJkZXRhaWwiOiAiYGV4Y2x1ZGUtcHItY3JlYXRlZC1iZWZvcmU6IFwiMjAyNi0xMS0xN1QwMDowMDowMFpcImAgZXhjbHVkZXMgZXZlcnkgUFIgY3JlYXRlZCBiZWZvcmUgdGhhdCB0aW1lc3RhbXAuIElmIHRoZSB3b3JrZmxvdyBpcyBtZXJnZWQgYW5kIGFjdGl2YXRlZCBiZWZvcmUgMjAyNi0xMS0xNywgYWxsIFBSc1x1MjAxNGluY2x1ZGluZyBvbmVzIG9wZW5lZCB0aGUgc2FtZSBkYXlcdTIwMTR3ZXJlIGNyZWF0ZWQgYmVmb3JlIHRoZSBjdXRvZmYsIHNvIG5laXRoZXIgdGhlIGBwdWxsX3JlcXVlc3RfdGFyZ2V0YCB0cmlnZ2VyIG5vciB0aGUgc2NoZWR1bGUgc3dlZXAgd291bGQgY2xvc2UgYW55dGhpbmcuIFRoZSB3b3JrZmxvdyB3b3VsZCBiZSBhIG5vLW9wIHVudGlsIHRoYXQgZGF0ZS4gSWYgMjAyNi0xMS0xNyBpcyB0aGUgaW50ZW5kZWQgZ28tbGl2ZSBkYXRlLCBjb25zaWRlciBhZGRpbmcgYSBjb21tZW50IHNheWluZyBzbzsgb3RoZXJ3aXNlIHNldCB0aGUgdmFsdWUgdG8gdGhlIGRhdGUgdGhlIGxvY2tkb3duIGlzIGFjdHVhbGx5IGVuYWJsZWQgb24gdGhlIG1pcnJvciBzbyB0aGF0IG5ldyBQUnMgYXJlIGNsb3NlZCBpbW1lZGlhdGVseS4iLCAicmVzcG9uc2UiOiAiIn1d -->
