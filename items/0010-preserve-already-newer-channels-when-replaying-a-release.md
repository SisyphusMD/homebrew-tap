# #10 Preserve already-newer channels when replaying a release

- Kind: issue, state: closed, by cody, created 2026-11-17T19:31:18-08:00
- Labels: none; milestone: none

Part of #3. A tagged publisher re-run can see a newer RC formula already on main. Preserve an unchanged newer formula and verify the requested release on every path being updated. If every path was superseded, return a no-op. This keeps old releases repairable without downgrading the tap or allowing unverified content into a PR. Dreame #302 and Whiskerless #224 will pin the fixed helper.
