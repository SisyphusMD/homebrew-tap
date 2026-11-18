# #9 Prove Tap required checks before protecting main

- Kind: issue, state: closed, by cody, created 2026-11-17T19:28:08-08:00
- Labels: none; milestone: none

Part of #3 and SisyphusMD/project-rules#76. Record the standard checks, Ruby syntax and generated formula provenance on a deliberate failing draft. Never merge the draft. Positive generated formula proof comes from the Dreame and Whiskerless publishers. Protection is still blocked until both release publishers prove their two PRs.

## cody, 2026-11-17T19:40:35-08:00

Draft #12 is proving expected failures on 799f8d2531829693c156eec396324a942ec85e89. It contains only synthetic fixtures and malformed Ruby and must never merge. The current publisher PRs still need a real ordered source-and-bottle proof.

## cody, 2026-11-17T19:46:14-08:00

Draft #12 at 799f8d2531829693c156eec396324a942ec85e89 deliberately failed all nine reported contexts. Verified exact diagnostics: missing issue reference, code without tests, diff over size, unused import, one synthetic scanner match, AI-review size refusal, formula changes outside the generated channel, and invalid Ruby. The draft is closed unmerged. Positive generated provenance and strict protection remain dependent on #3's publisher proof.

## cody, 2026-11-17T23:57:32-08:00

Closed failing draft #12 exercised every required context, including Ruby syntax and generated formula provenance. The exact heads of real publisher PRs #13, #14, #15 and #16 passed all checks. Verified strict main protection on e5b884b9779569f0919cae017e6d835a791bf042 with 8 required contexts. Direct pushes are disabled for all users, including admins. PRs must be up to date.
