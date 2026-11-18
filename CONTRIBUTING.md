# Contributing to the SisyphusMD Homebrew tap

Open [issues and pull requests on Forgejo][forge]. Sign in with GitHub and wait for account
activation. After activation, clone the Forgejo repository and send a pull request with AGit:

```sh
git push origin HEAD:refs/for/main -o topic=<short-name>
```

Use a Forgejo access token as the HTTPS password. Push again with the same topic to update the
pull request. GitHub serves a read-only mirror.

Read the [SisyphusMD project rules][project-rules] before contributing. Every pull request closes
an issue. Rule 9 excludes AI attribution, including a `Co-Authored-By` trailer for an assistant.
Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## Tests

The Forgejo Tests workflow checks each formula with `ruby -c` and tests the generated
release PR validator.

The release workflows in [dreame-valetudo][dreame] and [whiskerless][whiskerless] generate these
formulae and test their installation. Make generator changes there so the next release carries
them forward. For a tap change, include the source release or generator change and the result
of installing and running `brew test` on the affected formula. Use a `No tests: <reason>`
line for a generated formula change with no automated test changes.

## Generated releases

The source repository opens a formula PR after PyPI publishes the source archive.
After that PR lands, bottle jobs build against the formula on tap main and upload
the archives and manifests to the source release. The publisher then opens a
second PR for the bottle declarations. Both PRs reference the standing release
issue #6 and require the normal checks.

Before merging a generated PR, check that its head includes the current tip of
main and that Formula provenance passed for that head. If another PR landed while
this one was open, rerun the submit job to refresh against main and recheck it.
The publisher waits for the exact formula files on Forgejo before continuing.

**Safety-critical code** for rule 13: none.

## Required checks

`CI / Issue link (pull_request_target)`, `CI / Tests with code (pull_request_target)`,
`CI / Diff size (pull_request_target)`, `CI / Lint (pull_request_target)`,
`CI / Secrets (pull_request_target)`, `AI review` and
`Tests / Formula syntax (pull_request)`. Generated release PRs also require
`Tap release / Formula provenance (pull_request_target)`.

Each gate needs a passing and a failing run before it is added to branch protection.

## Break-glass

Rule 20 covers outages. For an urgent merge with Forgejo available, the maintainer can
remove the unavailable required context, restore it immediately after the merge, and record
the exception on the issue.

[forge]: https://forgejo.bryantserver.com/SisyphusMD/homebrew-tap
[project-rules]: https://forgejo.bryantserver.com/SisyphusMD/project-rules/src/branch/main/RULES.md
[dreame]: https://forgejo.bryantserver.com/SisyphusMD/dreame-valetudo
[whiskerless]: https://forgejo.bryantserver.com/SisyphusMD/whiskerless
