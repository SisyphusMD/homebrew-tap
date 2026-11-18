"""Exercise the release submitter using a local primary and API double."""

import contextlib
import runpy
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
submit = runpy.run_path(str(ROOT / ".forgejo/scripts/open-release-formula-pr.py"))["submit"]


class FormulaSubmissionTest(unittest.TestCase):
    def test_submits_only_candidate_and_reuses_pull_request(self):
        with tempfile.TemporaryDirectory() as scratch:
            fixture = Path(scratch)
            slug = "SisyphusMD/homebrew-tap"
            primary = fixture / f"{slug}.git"
            primary.parent.mkdir()
            checkout = fixture / "checkout"
            checkout.mkdir()
            artifact = fixture / "artifact"
            formula = Path("Formula/dreame-valetudo-rc.rb")
            (artifact / formula.parent).mkdir(parents=True)
            (artifact / formula).write_text("rendered formula\n")
            remote_root = fixture.as_uri()
            remote = f"{remote_root}/{slug}.git"

            def git(*args):
                return subprocess.check_output(
                    ["git", *args], cwd=checkout, text=True, stderr=subprocess.DEVNULL,
                ).strip()

            git("init", "--bare", str(primary))
            git("init", "-b", "main")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.test")
            git("config", "commit.gpgsign", "false")
            hooks = fixture / "empty-hooks"
            hooks.mkdir()
            git("config", "core.hooksPath", str(hooks))
            (checkout / formula.parent).mkdir()
            (checkout / formula).write_text("prior formula\n")
            git("add", str(formula))
            git("commit", "-m", "Base")
            git("remote", "add", "origin", remote)
            git("push", "origin", "main")
            main = git("rev-parse", "HEAD")
            known = []
            branch = "tap/dreame-valetudo/v0.3.0-rc.51/formula"

            def api(path, token, payload=None):
                self.assertEqual(token, "fixture")
                if path.startswith("/pulls?"):
                    return known
                self.assertEqual(path, "/pulls")
                self.assertEqual(payload["head"], branch)
                self.assertEqual(payload["base"], "main")
                self.assertFalse([pr for pr in known if pr["state"] == "open"], "must reuse the pending PR")
                record = {
                    "state": "open",
                    "merged": False,
                    "head": {"label": branch, "sha": git("ls-remote", "origin", branch).split()[0],
                             "repo": {"full_name": slug}},
                    "base": {"ref": "main"},
                    "html_url": "https://fixture.test/pulls/1",
                }
                known.append(record)
                return record

            def validate(ref, base, head):
                self.assertEqual(ref, branch)
                self.assertEqual(git("diff", "--name-only", base, head), str(formula))

            with (
                contextlib.chdir(checkout),
                patch.dict(submit.__globals__, {"FORGE": remote_root}),
                patch.dict(submit.__globals__["validation"], {"run": validate}),
            ):
                first = submit("dreame-valetudo", "v0.3.0-rc.51", "formula", artifact, "fixture", None, api)
                retry = submit("dreame-valetudo", "v0.3.0-rc.51", "formula", artifact, "fixture", None, api)
                self.assertEqual(first, {"state": "pending", "url": known[0]["html_url"]})
                self.assertEqual(retry, first)
                self.assertEqual(git("rev-parse", "HEAD"), main)
                self.assertEqual((checkout / formula).read_text(), "prior formula\n")
                self.assertEqual(git("ls-remote", "origin", "refs/heads/main").split()[0], main)
                self.assertEqual(git("ls-remote", "origin", f"refs/heads/{branch}").split()[0], known[0]["head"]["sha"])

                (checkout / "README.md").write_text("An unrelated change to main\n")
                git("add", "README.md")
                git("commit", "-m", "Advance main")
                git("push", "origin", "main")
                advanced = git("rev-parse", "HEAD")
                self.assertEqual(submit("dreame-valetudo", "v0.3.0-rc.51", "formula", artifact, "fixture", None, api),
                                 first)
                git("fetch", "origin", f"refs/heads/{branch}")
                self.assertEqual(git("rev-parse", "FETCH_HEAD^2"), advanced)

                # A same-tag repair may legitimately need a new PR after the original merged.
                git("merge", "--no-ff", "FETCH_HEAD", "-m", "Merge formula")
                git("push", "origin", "main", f":refs/heads/{branch}")
                known[0].update(state="closed", merged=True)
                (artifact / formula).write_text("repaired formula\n")
                submit("dreame-valetudo", "v0.3.0-rc.51", "formula", artifact, "fixture", None, api)
                self.assertEqual(len(known), 2)
