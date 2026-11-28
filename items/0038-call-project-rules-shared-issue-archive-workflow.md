# #38 Call project-rules' shared issue-archive workflow

- Kind: issue, state: closed, by cody, created 2026-11-27T07:01:29-08:00
- Labels: status:in-progress, type:chore; milestone: none

project-rules now runs the issue-archive job from its main (SisyphusMD/project-rules#144). Replace this repo's .forgejo/workflows/issue-archive.yml with the new caller and delete .forgejo/scripts/issue-archive.py, which no longer runs and fell behind main.

## cody, 2026-11-27T07:14:02-08:00

Done: #39 merged and verified; a dispatched Issue archive run went through the shared workflow and pushed the archive branch. Branch removed.
