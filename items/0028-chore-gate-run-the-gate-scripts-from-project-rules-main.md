# #28 chore(gate): run the gate scripts from project-rules main

- Kind: pull, state: closed, by cody, created 2026-11-24T17:59:12-08:00
- Labels: none; milestone: none
- refs/pull/28/head -> main, merged: True

Closes #27

This repo ran its own copies of the gate scripts, so a fix in project-rules needed a PR here. `ci.yml` and `ai-review.yml` are now project-rules main's (26da87ec), which fetch the scripts from project-rules main on every run and fail when they cannot. The four copies are removed; `check-release-formulae.py`, `open-release-formula-pr.py` and `issue-archive.py` stay. `mirror-lockdown.yml` and `.forgejo/RULES.md` are copied again from the same commit.

Large diff: 772 of the removed lines are the four deleted script copies, and the added lines are copied from project-rules main, where they were reviewed and tested.

The check jobs run from main, so this PR is judged by the old copies. The next PR proves the new ones.


## forgejo-actions, 2026-11-24T17:59:50-08:00

<!-- ai-review -->
**AI review** of `8eaff72d7d`: The PR correctly switches gate scripts to project-rules main per issue #27 and the project-rules#78 decision. The RULES.md whole-file sync is justified by rule 22 and explicitly scoped by the issue's latest comment. No new issues found.

### Withdrawn

- **F1** (blocking, `.forgejo/RULES.md:113`) Unrelated 'Automatic memory sync' section bundled into this PR: The new exception table row and the '### Automatic memory sync' section (lines 113–124) concern issue #101 (memory sync), not issue #27 (run gate scripts from project-rules main). Rule 7 requires every hunk to map to the issue or to something the change cannot work without; this section does neither. The rule 15 wording update is fine—it describes the new script-fetching mechanism. Remove the memory-sync rows and section from this PR and land them in a separate PR that closes #101.
  - Reviewer: Withdrawn. Rule 22 requires `.forgejo/RULES.md` to be a synced copy of the whole file, and issue #27's latest comment explicitly scopes the sync to commit 26da87ec (the same commit the workflows come from). The memory-sync section landed in project-rules under its own issue (#101) and is already in force; partial syncing would produce a file matching no version of the rules, violating rule 22. This is a project decision, not an unrelated change.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZm9yZ2Vqby9SVUxFUy5tZCIsICJsaW5lIjogMTEzLCAic2V2ZXJpdHkiOiAiYmxvY2tpbmciLCAic3RhdHVzIjogIndpdGhkcmF3biIsICJ0aXRsZSI6ICJVbnJlbGF0ZWQgJ0F1dG9tYXRpYyBtZW1vcnkgc3luYycgc2VjdGlvbiBidW5kbGVkIGludG8gdGhpcyBQUiIsICJkZXRhaWwiOiAiVGhlIG5ldyBleGNlcHRpb24gdGFibGUgcm93IGFuZCB0aGUgJyMjIyBBdXRvbWF0aWMgbWVtb3J5IHN5bmMnIHNlY3Rpb24gKGxpbmVzIDExM1x1MjAxMzEyNCkgY29uY2VybiBpc3N1ZSAjMTAxIChtZW1vcnkgc3luYyksIG5vdCBpc3N1ZSAjMjcgKHJ1biBnYXRlIHNjcmlwdHMgZnJvbSBwcm9qZWN0LXJ1bGVzIG1haW4pLiBSdWxlIDcgcmVxdWlyZXMgZXZlcnkgaHVuayB0byBtYXAgdG8gdGhlIGlzc3VlIG9yIHRvIHNvbWV0aGluZyB0aGUgY2hhbmdlIGNhbm5vdCB3b3JrIHdpdGhvdXQ7IHRoaXMgc2VjdGlvbiBkb2VzIG5laXRoZXIuIFRoZSBydWxlIDE1IHdvcmRpbmcgdXBkYXRlIGlzIGZpbmVcdTIwMTRpdCBkZXNjcmliZXMgdGhlIG5ldyBzY3JpcHQtZmV0Y2hpbmcgbWVjaGFuaXNtLiBSZW1vdmUgdGhlIG1lbW9yeS1zeW5jIHJvd3MgYW5kIHNlY3Rpb24gZnJvbSB0aGlzIFBSIGFuZCBsYW5kIHRoZW0gaW4gYSBzZXBhcmF0ZSBQUiB0aGF0IGNsb3NlcyAjMTAxLiIsICJyZXNwb25zZSI6ICJXaXRoZHJhd24uIFJ1bGUgMjIgcmVxdWlyZXMgYC5mb3JnZWpvL1JVTEVTLm1kYCB0byBiZSBhIHN5bmNlZCBjb3B5IG9mIHRoZSB3aG9sZSBmaWxlLCBhbmQgaXNzdWUgIzI3J3MgbGF0ZXN0IGNvbW1lbnQgZXhwbGljaXRseSBzY29wZXMgdGhlIHN5bmMgdG8gY29tbWl0IDI2ZGE4N2VjICh0aGUgc2FtZSBjb21taXQgdGhlIHdvcmtmbG93cyBjb21lIGZyb20pLiBUaGUgbWVtb3J5LXN5bmMgc2VjdGlvbiBsYW5kZWQgaW4gcHJvamVjdC1ydWxlcyB1bmRlciBpdHMgb3duIGlzc3VlICgjMTAxKSBhbmQgaXMgYWxyZWFkeSBpbiBmb3JjZTsgcGFydGlhbCBzeW5jaW5nIHdvdWxkIHByb2R1Y2UgYSBmaWxlIG1hdGNoaW5nIG5vIHZlcnNpb24gb2YgdGhlIHJ1bGVzLCB2aW9sYXRpbmcgcnVsZSAyMi4gVGhpcyBpcyBhIHByb2plY3QgZGVjaXNpb24sIG5vdCBhbiB1bnJlbGF0ZWQgY2hhbmdlLiJ9XQ== -->

## cody, 2026-11-24T18:00:34-08:00

F1: `.forgejo/RULES.md` is, by rule 22, "a synced copy of this file", so it is copied whole from project-rules main at the commit the workflows come from. The memory-sync exception is not a change made here: it landed in project-rules under its own issue there (project-rules#101, not an issue in this repo) and is already in force for every repo. Copying only the rule 15 hunk would leave a file that matches no version of the rules. #27 did not say this; its latest comment now puts the sync in scope.
