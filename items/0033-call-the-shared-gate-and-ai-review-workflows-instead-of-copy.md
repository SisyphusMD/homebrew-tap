# #33 Call the shared gate and AI review workflows instead of copying them

- Kind: issue, state: closed, by cody, created 2026-11-25T18:43:14-08:00
- Labels: status:in-progress, type:chore; milestone: none

Pilot for SisyphusMD/project-rules#78: this repo's ci.yml and ai-review.yml become small callers of project-rules main's gate.yml, gate-lint.yml and review.yml (project-rules#129), so the jobs stop being copies here. Check names stay the same. After it merges, one PR here is proven failing and then passing on the called jobs before any other repo switches.

Claude has this.

## cody, 2026-11-25T21:19:58-08:00

Landed in #34 (8512d261). Proven on proof PR #35, closed unmerged: with no issue named, CI / Issue link (pull_request_target) failed (run 47766); after the description named #33 every required check passed under its usual name (run 47811), the fork guard ran, and a maintainer reply re-ran the review through the called workflow (run 47842). Each caller adds CI / shared-gate, CI / shared-lint and AI review / shared-review, which nothing requires.
