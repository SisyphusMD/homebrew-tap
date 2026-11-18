# #2 Adopt the SisyphusMD project rules

- Kind: pull, state: closed, by cody, created 2026-11-17T14:09:37-08:00
- Labels: none; milestone: none
- refs/pull/2/head -> main, merged: True

Closes #1

Add the shared Forgejo checks, templates, issue archive and private security reporting. Add a read-only Ruby syntax check for the generated formulae.

Large diff: the shared workflows, scripts, templates and rules are copied verbatim from project-rules.

Validated locally with Ruby syntax checks on all three formulae, actionlint, Ruff, yamllint and the pinned history scan.

GitHub mirror lockdown follows after checking the mirror token's permission to write workflow files. Branch protection is tracked on the project-rules adoption issue.
