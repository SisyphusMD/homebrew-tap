# #34 chore(gate): call the shared gate and AI review workflows

- Kind: pull, state: closed, by cody, created 2026-11-25T18:44:18-08:00
- Labels: none; milestone: none
- refs/pull/34/head -> main, merged: True

Closes #33

`ci.yml` and `ai-review.yml` carried copies of the gate and AI review jobs, and copies drift. They now call project-rules main's `gate.yml`, `gate-lint.yml` and `review.yml` (SisyphusMD/project-rules#78, #129) and keep only what a called workflow cannot hold: the triggers, the concurrency groups and the one secret the jobs may see, `ISSUE_READ_TOKEN`. Check names stay the same; each calling job adds one check of its own (`CI / shared-gate` and so on), which nothing requires.

This PR is judged by the old copies, because `pull_request_target` runs main's files. The pilot proof comes after it merges: one PR here failing and then passing on the called jobs, before any other repo switches.

No tests: workflow wiring only, checked by project-rules' tests of the called files and by the proof PR after merge.


## forgejo-actions, 2026-11-25T18:44:50-08:00

<!-- ai-review -->
**AI review** of `9265904020`: Clean refactoring that replaces inline gate/review job copies with calls to shared reusable workflows in project-rules. The caller files retain only triggers, concurrency, and the one non-auto secret. No correctness, security, or test issues found.

### Resolved

- **F1** (suggestion, `.forgejo/workflows/ci.yml:5`) Comment contradicts itself: "no repo carries a copy" vs "repos get a copy": The added sentence "Only this caller is copied" now bridges the two statements: "no repo copies the jobs" refers to the job implementations, while "repos get a copy" refers to this thin caller file. The contradiction is resolved.


Disagree? Reply on this PR with your reasoning; the reviewer re-reads every reply.
<!-- ai-review-state W3siaWQiOiAiRjEiLCAiZmlsZSI6ICIuZm9yZ2Vqby93b3JrZmxvd3MvY2kueW1sIiwgImxpbmUiOiA1LCAic2V2ZXJpdHkiOiAic3VnZ2VzdGlvbiIsICJzdGF0dXMiOiAicmVzb2x2ZWQiLCAidGl0bGUiOiAiQ29tbWVudCBjb250cmFkaWN0cyBpdHNlbGY6IFwibm8gcmVwbyBjYXJyaWVzIGEgY29weVwiIHZzIFwicmVwb3MgZ2V0IGEgY29weVwiIiwgImRldGFpbCI6ICJUaGUgYWRkZWQgc2VudGVuY2UgXCJPbmx5IHRoaXMgY2FsbGVyIGlzIGNvcGllZFwiIG5vdyBicmlkZ2VzIHRoZSB0d28gc3RhdGVtZW50czogXCJubyByZXBvIGNvcGllcyB0aGUgam9ic1wiIHJlZmVycyB0byB0aGUgam9iIGltcGxlbWVudGF0aW9ucywgd2hpbGUgXCJyZXBvcyBnZXQgYSBjb3B5XCIgcmVmZXJzIHRvIHRoaXMgdGhpbiBjYWxsZXIgZmlsZS4gVGhlIGNvbnRyYWRpY3Rpb24gaXMgcmVzb2x2ZWQuIiwgInJlc3BvbnNlIjogIiJ9XQ== -->
