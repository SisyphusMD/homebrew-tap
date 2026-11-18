"""Check version, source provenance, and bottle phase ordering without network access."""

import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
verify = runpy.run_path(str(ROOT / ".forgejo/scripts/check-release-formulae.py"))["verify_formulae"]
PROJECT = "dreame-valetudo"
PATH = f"Formula/{PROJECT}-rc.rb"
TAG = "v0.3.0-rc.51"
ASSET_BASE = f"https://forgejo.bryantserver.com/SisyphusMD/{PROJECT}/releases/download/{TAG}"
CHECKSUM = "1" * 64
PLATFORMS = {"arm64_sequoia": "2" * 64, "arm64_linux": "3" * 64, "x86_64_linux": "4" * 64}
SDIST = "dreame_valetudo-0.3.0rc51.tar.gz"
SOURCE = f'  url "https://files.pythonhosted.org/packages/source/d/{PROJECT}/{SDIST}"\n  sha256 "{CHECKSUM}"\n'
TEMPLATE = SOURCE.replace("0.3.0rc51", "REPLACE_VERSION").replace(CHECKSUM, "REPLACE_TARBALL_SHA256")
TEMPLATE += "REPLACE_BOTTLE_BLOCK\n"
BOTTLED = SOURCE + f'\n  bottle do\n    root_url "{ASSET_BASE}"\n' + "".join(
    f'    sha256 cellar: :any, {platform}: "{digest}"\n' for platform, digest in PLATFORMS.items()
) + "  end\n\n"
SOURCE += "\n"


def metadata(url):
    if url.startswith("https://pypi.org/"):
        return {"urls": [{"packagetype": "sdist", "filename": SDIST, "digests": {"sha256": CHECKSUM}}]}
    if url.endswith(f"/tags/{TAG}"):
        return {"tag_name": TAG, "assets": [
            {"name": "manifest.bottle.json", "browser_download_url": f"{ASSET_BASE}/manifest.bottle.json"},
            *({"name": f"{platform}.bottle.tar.gz",
               "browser_download_url": f"{ASSET_BASE}/{platform}.bottle.tar.gz"} for platform in PLATFORMS),
        ]}
    if url == f"{ASSET_BASE}/manifest.bottle.json":
        return {f"sisyphusmd/tap/{PROJECT}-rc": {"formula": {"pkg_version": "0.3.0rc51"},
                "bottle": {"cellar": "any", "tags": {
            platform: {"filename": f"{platform}.bottle.tar.gz", "sha256": digest}
            for platform, digest in PLATFORMS.items()
        }}}}
    raise AssertionError(url)


def verify_fixture(phase, before, after, changed=None):
    verify(
        PROJECT, TAG, phase, before, after, changed or {PATH}, metadata, lambda _: TEMPLATE,
        lambda url: PLATFORMS[url.rsplit("/", 1)[-1].split(".")[0]],
    )


class ReleaseFormulaTest(unittest.TestCase):
    def test_formula_then_bottles(self):
        verify_fixture("formula", {}, {PATH: SOURCE})
        verify_fixture("bottles", {PATH: SOURCE}, {PATH: BOTTLED})

    def test_bottles_require_their_exact_source_on_main(self):
        for before in ({}, {PATH: SOURCE.replace("rc51", "rc50")}):
            with self.subTest(before=before), self.assertRaisesRegex(ValueError, "matching source formula"):
                verify_fixture("bottles", before, {PATH: BOTTLED})

    def test_downgrade_and_wrong_bottle_root_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "replace a newer release"):
            verify_fixture("formula", {PATH: SOURCE.replace("rc51", "rc52")}, {PATH: SOURCE})
        bad_bottle = BOTTLED.replace(TAG, "v0.3.0-rc.50")
        with self.assertRaisesRegex(ValueError, "three bottles"):
            verify_fixture("bottles", {PATH: SOURCE}, {PATH: bad_bottle})

    def test_release_cannot_change_another_formula(self):
        with self.assertRaisesRegex(ValueError, "outside its formula channel"):
            verify_fixture("formula", {}, {PATH: SOURCE}, {PATH, "Formula/whiskerless-rc.rb"})

    def test_release_cannot_add_unexpected_ruby(self):
        with self.assertRaisesRegex(ValueError, "tagged formula template"):
            verify_fixture("formula", {}, {PATH: SOURCE + '  url  "https://example.test/source.tar.gz"\n'})
        with self.assertRaisesRegex(ValueError, "three bottles"):
            verify_fixture("bottles", {PATH: SOURCE},
                           {PATH: BOTTLED.replace("  end\n", '    root_url  "https://example.test"\n  end\n')})

    def test_already_superseded_rc_is_untouched(self):
        live = {PATH: SOURCE.replace("rc51", "rc52")}
        verify(PROJECT, TAG, "formula", live, live, {PATH}, fetch=lambda _: self.fail("superseded tag was fetched"))

    def test_stable_can_advance_without_replacing_newer_candidate(self):
        requested = "v0.3.0"
        stable_path = f"Formula/{PROJECT}.rb"
        newer_rc = SOURCE.replace("0.3.0rc51", "0.4.0rc1")
        stable = SOURCE.replace("0.3.0rc51", "0.3.0")
        before = {PATH: newer_rc}
        after = {PATH: newer_rc, stable_path: stable}
        pypi = {"urls": [{"packagetype": "sdist", "filename": SDIST.replace("rc51", ""),
                          "digests": {"sha256": CHECKSUM}}]}
        verify(PROJECT, requested, "formula", before, after, {stable_path}, lambda _: pypi, lambda _: TEMPLATE)
        with self.assertRaisesRegex(ValueError, "replace a newer release"):
            verify(PROJECT, requested, "formula", before, {stable_path: stable, PATH: stable},
                   {stable_path, PATH}, lambda _: pypi, lambda _: TEMPLATE)
