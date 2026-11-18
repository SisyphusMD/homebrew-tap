# #3 Publish formula updates through pull requests

- Kind: issue, state: closed, by cody, created 2026-11-17T14:18:45-08:00
- Labels: status:in-progress, type:feature; milestone: none

Part of SisyphusMD/project-rules#86 and #1 here. Move the Dreame and Whiskerless formula/bottle publishers to PRs so tap main can reject direct pushes. Preserve formula and bottle order, provenance, and retry behavior. Prove both publishers before enabling protection.

## cody, 2026-11-17T18:16:07-08:00

Codex is mapping the existing two-pass formula/bottle handshake before changing any publisher. Generated update issue #6 will be the stable PR reference.

## cody, 2026-11-17T20:40:39-08:00

Publisher code is ready. dreame-valetudo #303 and whiskerless #227 both merged with green exact-head checks and verified mirrors. Both pin Tap #11 at c8bb9a5b3a54c841375a5a3b619c98a377cb75be. Tap draft #12 verified the negative checks and is closed.

Blocked on Cody’s approval to publish Dreame v0.3.0-rc.52 and Whiskerless v0.2.0-rc.78. Once approved, do one candidate at a time. Verify source formula PR, bottle build, bottle PR and install in order, then require current-branch protection and all verified contexts.

## cody, 2026-11-17T22:50:18-08:00

Decision: Publish Dreame v0.3.0-rc.52 and Whiskerless v0.2.0-rc.78 for live Tap verification. Why: Cody said “Do it then” after the rollout reported those two pending public prereleases.

Decided by: Cody, 2026-11-17.

## cody, 2026-11-17T23:57:32-08:00

Dreame v0.3.0-rc.52 generated formula PR #13 and bottles PR #14. Its exact-tag install matrix passed on both Linux architectures and both macOS versions, including the bottle pours.

https://forgejo.bryantserver.com/SisyphusMD/dreame-valetudo/actions/runs/1835

Whiskerless v0.2.0-rc.78 generated formula PR #15 and bottles PR #16. Its exact-tag install matrix passed on both Linux architectures and both macOS versions, including the bottle pours.

https://forgejo.bryantserver.com/SisyphusMD/whiskerless/actions/runs/1417

The formula PR landed before bottle builds in both releases. All four generated PRs passed the provenance check. Independently verified all 18 bottle downloads across Forgejo, NAS and GitHub against the merged formulas. Both Tap mirrors match. Verified strict main protection on e5b884b9779569f0919cae017e6d835a791bf042 with 8 required contexts. Direct pushes are disabled for all users, including admins. PRs must be up to date.
