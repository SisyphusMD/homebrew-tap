# #11 Preserve newer tap channels when replaying a release

- Kind: pull, state: closed, by cody, created 2026-11-17T19:35:37-08:00
- Labels: none; milestone: none
- refs/pull/11/head -> main, merged: True

Closes #10. Refs #3.

Recognize a no-op only when every rendered file equals an already-newer file on main. A stable candidate may update its stable formula while keeping the exact newer RC formula. Keep validating every changed path and have the caller wait only for the paths the PR actually changes.

Eight local tests and Ruff passed. The release fixtures verify an unchanged newer RC, stable-only updates and rejection of replacing a newer formula.

## forgejo-actions, 2026-11-17T19:41:51-08:00

<!-- ai-review -->
**AI review** of `3f539c9387`: The PR correctly preserves newer RC formulae during stable replays, adds a 'superseded' state, and returns changed paths for callers. The previously-flagged missing test for the superseded branch is now covered by the new test_superseded_formula_does_not_open_a_pr_or_push test, and the verify_formulae logic is exercised by two additional tests.

### Resolved

- **F1** (blocking, `.forgejo/scripts/open-release-formula-pr.py:91`) No test for the new 'superseded' state returned by submit(): The submit() function now returns {"state": "superseded"} when every rendered path is an already-newer formula on main. This is a new caller-visible contract (previously this scenario returned "landed"). Rule 12 requires a test for every new behaviour. The existing test_already_superseded_rc_is_untouched exercises verify_formulae's early return, but nothing drives submit() through the `if not still_current: return {"state": "superseded"}` branch. Add a test in test_formula_submission.py that sets up a base whose formula version is newer than the requested tag, calls submit(), and asserts the return is {"state": "superseded"} with no push or PR creation.
  - Reviewer: Resolved by the new test_superseded_formula_does_not_open_a_pr_or_push, which patches current_values to return identical content (making changed empty), lets the real untouched_newer_formulae identify the rc52 formula as newer than the requested rc51 tag, and asserts the return is {"state": "superseded"} with the api callable set to self.fail to prove no PR API contact.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZm9yZ2Vqby9zY3JpcHRzL29wZW4tcmVsZWFzZS1mb3JtdWxhLXByLnB5IiwgImxpbmUiOiA5MSwgInNldmVyaXR5IjogImJsb2NraW5nIiwgInN0YXR1cyI6ICJyZXNvbHZlZCIsICJ0aXRsZSI6ICJObyB0ZXN0IGZvciB0aGUgbmV3ICdzdXBlcnNlZGVkJyBzdGF0ZSByZXR1cm5lZCBieSBzdWJtaXQoKSIsICJkZXRhaWwiOiAiVGhlIHN1Ym1pdCgpIGZ1bmN0aW9uIG5vdyByZXR1cm5zIHtcInN0YXRlXCI6IFwic3VwZXJzZWRlZFwifSB3aGVuIGV2ZXJ5IHJlbmRlcmVkIHBhdGggaXMgYW4gYWxyZWFkeS1uZXdlciBmb3JtdWxhIG9uIG1haW4uIFRoaXMgaXMgYSBuZXcgY2FsbGVyLXZpc2libGUgY29udHJhY3QgKHByZXZpb3VzbHkgdGhpcyBzY2VuYXJpbyByZXR1cm5lZCBcImxhbmRlZFwiKS4gUnVsZSAxMiByZXF1aXJlcyBhIHRlc3QgZm9yIGV2ZXJ5IG5ldyBiZWhhdmlvdXIuIFRoZSBleGlzdGluZyB0ZXN0X2FscmVhZHlfc3VwZXJzZWRlZF9yY19pc191bnRvdWNoZWQgZXhlcmNpc2VzIHZlcmlmeV9mb3JtdWxhZSdzIGVhcmx5IHJldHVybiwgYnV0IG5vdGhpbmcgZHJpdmVzIHN1Ym1pdCgpIHRocm91Z2ggdGhlIGBpZiBub3Qgc3RpbGxfY3VycmVudDogcmV0dXJuIHtcInN0YXRlXCI6IFwic3VwZXJzZWRlZFwifWAgYnJhbmNoLiBBZGQgYSB0ZXN0IGluIHRlc3RfZm9ybXVsYV9zdWJtaXNzaW9uLnB5IHRoYXQgc2V0cyB1cCBhIGJhc2Ugd2hvc2UgZm9ybXVsYSB2ZXJzaW9uIGlzIG5ld2VyIHRoYW4gdGhlIHJlcXVlc3RlZCB0YWcsIGNhbGxzIHN1Ym1pdCgpLCBhbmQgYXNzZXJ0cyB0aGUgcmV0dXJuIGlzIHtcInN0YXRlXCI6IFwic3VwZXJzZWRlZFwifSB3aXRoIG5vIHB1c2ggb3IgUFIgY3JlYXRpb24uIiwgInJlc3BvbnNlIjogIlJlc29sdmVkIGJ5IHRoZSBuZXcgdGVzdF9zdXBlcnNlZGVkX2Zvcm11bGFfZG9lc19ub3Rfb3Blbl9hX3ByX29yX3B1c2gsIHdoaWNoIHBhdGNoZXMgY3VycmVudF92YWx1ZXMgdG8gcmV0dXJuIGlkZW50aWNhbCBjb250ZW50IChtYWtpbmcgY2hhbmdlZCBlbXB0eSksIGxldHMgdGhlIHJlYWwgdW50b3VjaGVkX25ld2VyX2Zvcm11bGFlIGlkZW50aWZ5IHRoZSByYzUyIGZvcm11bGEgYXMgbmV3ZXIgdGhhbiB0aGUgcmVxdWVzdGVkIHJjNTEgdGFnLCBhbmQgYXNzZXJ0cyB0aGUgcmV0dXJuIGlzIHtcInN0YXRlXCI6IFwic3VwZXJzZWRlZFwifSB3aXRoIHRoZSBhcGkgY2FsbGFibGUgc2V0IHRvIHNlbGYuZmFpbCB0byBwcm92ZSBubyBQUiBBUEkgY29udGFjdC4ifV0= -->
