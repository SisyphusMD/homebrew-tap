# #24 chore(ci): copy the AI review from project-rules 0e929cc

- Kind: pull, state: closed, by cody, created 2026-11-21T18:33:27-08:00
- Labels: none; milestone: none
- refs/pull/24/head -> main, merged: True

Closes #23

Both files are byte-for-byte canonical SisyphusMD/project-rules 0e929cc. This is the first copy with the pinned checkout, so its own AI review run is the first live pull_request_target test of `ref: ${{ github.sha }}` (the checkout log names the commit; it must be main, not the PR head).

## forgejo-actions, 2026-11-21T18:35:41-08:00

<!-- ai-review -->
**AI review** of `181c36a21a`: Verbatim copy of the AI review script and workflow from project-rules 0e929cc, adding connect-retry, malformed-answer re-ask with strict schema, bounded replies, and a base-commit checkout pin. The code is well-structured and I found no correctness or security bugs in the new logic; the only outstanding item is the missing test justification line.

### Open

- **F1** (suggestion, `.forgejo/scripts/ai-review.py:1`) No tests and no `No tests:` line for new behaviour: Rule 12 requires every feature or fix to ship with tests. This PR adds connect-retry, the re-ask-with-schema path, bounded replies, and the `ref: github.sha` checkout pin, but includes no test file and no `No tests:` line in the description. Because the code is a byte-for-byte copy from project-rules 0e929cc (where its tests live) and this repo's CONTRIBUTING.md establishes no test harness for CI Python scripts, a `No tests: verbatim copy from project-rules 0e929cc; tested there` line in the PR description would satisfy the rule without inventing a new test framework here.
  - Reviewer: The PR description states the files are byte-for-byte canonical copies, which is the right justification, but rule 12's mechanism for recording 'no tests here because they live elsewhere' is the `No tests:` line. Adding one (e.g. `No tests: verbatim copy from project-rules 0e929cc; tested there`) makes the exemption explicit and machine-checkable without requiring a new test harness in this repo.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZm9yZ2Vqby9zY3JpcHRzL2FpLXJldmlldy5weSIsICJsaW5lIjogMSwgInNldmVyaXR5IjogInN1Z2dlc3Rpb24iLCAic3RhdHVzIjogIm9wZW4iLCAidGl0bGUiOiAiTm8gdGVzdHMgYW5kIG5vIGBObyB0ZXN0czpgIGxpbmUgZm9yIG5ldyBiZWhhdmlvdXIiLCAiZGV0YWlsIjogIlJ1bGUgMTIgcmVxdWlyZXMgZXZlcnkgZmVhdHVyZSBvciBmaXggdG8gc2hpcCB3aXRoIHRlc3RzLiBUaGlzIFBSIGFkZHMgY29ubmVjdC1yZXRyeSwgdGhlIHJlLWFzay13aXRoLXNjaGVtYSBwYXRoLCBib3VuZGVkIHJlcGxpZXMsIGFuZCB0aGUgYHJlZjogZ2l0aHViLnNoYWAgY2hlY2tvdXQgcGluLCBidXQgaW5jbHVkZXMgbm8gdGVzdCBmaWxlIGFuZCBubyBgTm8gdGVzdHM6YCBsaW5lIGluIHRoZSBkZXNjcmlwdGlvbi4gQmVjYXVzZSB0aGUgY29kZSBpcyBhIGJ5dGUtZm9yLWJ5dGUgY29weSBmcm9tIHByb2plY3QtcnVsZXMgMGU5MjljYyAod2hlcmUgaXRzIHRlc3RzIGxpdmUpIGFuZCB0aGlzIHJlcG8ncyBDT05UUklCVVRJTkcubWQgZXN0YWJsaXNoZXMgbm8gdGVzdCBoYXJuZXNzIGZvciBDSSBQeXRob24gc2NyaXB0cywgYSBgTm8gdGVzdHM6IHZlcmJhdGltIGNvcHkgZnJvbSBwcm9qZWN0LXJ1bGVzIDBlOTI5Y2M7IHRlc3RlZCB0aGVyZWAgbGluZSBpbiB0aGUgUFIgZGVzY3JpcHRpb24gd291bGQgc2F0aXNmeSB0aGUgcnVsZSB3aXRob3V0IGludmVudGluZyBhIG5ldyB0ZXN0IGZyYW1ld29yayBoZXJlLiIsICJyZXNwb25zZSI6ICJUaGUgUFIgZGVzY3JpcHRpb24gc3RhdGVzIHRoZSBmaWxlcyBhcmUgYnl0ZS1mb3ItYnl0ZSBjYW5vbmljYWwgY29waWVzLCB3aGljaCBpcyB0aGUgcmlnaHQganVzdGlmaWNhdGlvbiwgYnV0IHJ1bGUgMTIncyBtZWNoYW5pc20gZm9yIHJlY29yZGluZyAnbm8gdGVzdHMgaGVyZSBiZWNhdXNlIHRoZXkgbGl2ZSBlbHNld2hlcmUnIGlzIHRoZSBgTm8gdGVzdHM6YCBsaW5lLiBBZGRpbmcgb25lIChlLmcuIGBObyB0ZXN0czogdmVyYmF0aW0gY29weSBmcm9tIHByb2plY3QtcnVsZXMgMGU5MjljYzsgdGVzdGVkIHRoZXJlYCkgbWFrZXMgdGhlIGV4ZW1wdGlvbiBleHBsaWNpdCBhbmQgbWFjaGluZS1jaGVja2FibGUgd2l0aG91dCByZXF1aXJpbmcgYSBuZXcgdGVzdCBoYXJuZXNzIGluIHRoaXMgcmVwby4ifV0= -->
