"""Verify that a generated tap PR matches its source release and updates the right channel."""

import hashlib
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

FORGE = "https://forgejo.bryantserver.com"
OWNER = "SisyphusMD"
PROJECTS = {"dreame-valetudo", "whiskerless"}
NUMBER = r"(?:0|[1-9][0-9]*)"
TAG = rf"v{NUMBER}\.{NUMBER}\.{NUMBER}(?:-rc\.[1-9][0-9]*)?"
REF = re.compile(rf"tap/([a-z-]+)/({TAG})/(formula|bottles)")
SHA = re.compile(r"[0-9a-f]{40}")
HASH = r"[0-9a-f]{64}"
BOTTLE = re.compile(r"^  bottle do\n(.*?)^  end\n", re.MULTILINE | re.DOTALL)
PLATFORMS = {"arm64_sequoia", "arm64_linux", "x86_64_linux"}


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def load_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SisyphusMD Homebrew release verification"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def load_text(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read(100_001).decode("utf-8")


def asset_digest(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return hashlib.file_digest(response, "sha256").hexdigest()


def project_paths(project, tag):
    names = {f"{project}-rc"}
    if "-rc." not in tag:
        names.add(project)
    return {f"Formula/{name}.rb" for name in names}


def formula_source(content):
    url = re.findall(r'^  url "([^"]+)"$', content, re.MULTILINE)
    checksum = re.findall(rf'^  sha256 "({HASH})"$', content, re.MULTILINE)
    if len(url) != 1 or len(checksum) != 1:
        raise ValueError("expected exactly one formula source URL and SHA-256")
    return url[0], checksum[0]


def version_key(project, url):
    basename = PurePosixPath(urllib.parse.urlsplit(url).path).name
    stem = re.escape(project.replace("-", "_"))
    match = re.fullmatch(
        rf"(?:{stem}-|v)({NUMBER})\.({NUMBER})\.({NUMBER})(?:-?rc\.?([1-9][0-9]*))?\.tar\.gz",
        basename,
    )
    if match is None:
        raise ValueError(f"unrecognized source archive for {project}")
    major, minor, patch = map(int, match.groups()[:3])
    rc = match[4]
    return major, minor, patch, rc is None, int(rc or 0)


def bottle_block(content):
    blocks = BOTTLE.findall(content)
    if len(blocks) > 1:
        raise ValueError("multiple bottle blocks")
    return blocks[0] if blocks else ""


def source_digest(project, tag, fetch):
    version = tag[1:].replace("-rc.", "rc")
    expected = f"{project.replace('-', '_')}-{version}.tar.gz"
    metadata = fetch(f"https://pypi.org/pypi/{project}/{version}/json")
    digests = {row["digests"]["sha256"] for row in metadata["urls"]
               if row["packagetype"] == "sdist" and row["filename"] == expected}
    if len(digests) != 1:
        raise ValueError(f"PyPI must publish one source digest for {expected}")
    return expected, digests.pop()


def release_bottles(project, tag, fetch, digest_asset):
    release = fetch(f"{FORGE}/api/v1/repos/{OWNER}/{project}/releases/tags/{tag}")
    if release["tag_name"] != tag:
        raise ValueError("wrong Forgejo release")
    root = f"{FORGE}/{OWNER}/{project}/releases/download/{tag}/"
    assets = {row["name"]: row["browser_download_url"] for row in release["assets"]}
    if any(url != root + urllib.parse.quote(name) for name, url in assets.items()):
        raise ValueError("bottle asset URL leaves the source release")
    bottles = {}
    checked_assets = {}
    for asset in release["assets"]:
        if not asset["name"].endswith(".bottle.json"):
            continue
        url = asset["browser_download_url"]
        manifest = fetch(url)
        for name, record in manifest.items():
            if record["formula"]["pkg_version"] != tag[1:].replace("-rc.", "rc") or record["bottle"].get("rebuild", 0):
                raise ValueError(f"manifest is for the wrong version or rebuild of {name}")
            for platform, info in record["bottle"]["tags"].items():
                filename = info["filename"]
                if filename not in assets:
                    raise ValueError(f"missing bottle asset {filename}")
                digest = info["sha256"]
                if filename not in checked_assets:
                    checked_assets[filename] = digest_asset(assets[filename])
                if checked_assets[filename] != digest:
                    raise ValueError(f"published archive does not match the manifest for {filename}")
                checksums = bottles.setdefault(name, {})
                entry = (digest, record["bottle"]["cellar"])
                if platform in checksums and checksums[platform] != entry:
                    raise ValueError(f"conflicting manifests for {name} {platform}")
                checksums[platform] = entry
    return bottles


def render_template(template, tag, digest, block=""):
    version = tag[1:].replace("-rc.", "rc")
    if template.count("REPLACE_BOTTLE_BLOCK\n") != 1:
        raise ValueError("tagged formula template has no unique bottle marker")
    replacement = f"\n  bottle do\n{block}  end\n\n" if block else "\n"
    return (template.replace("REPLACE_PYPI_VERSION", version).replace("REPLACE_VERSION", version)
            .replace("REPLACE_SDIST_SHA256", digest).replace("REPLACE_TARBALL_SHA256", digest)
            .replace("REPLACE_BOTTLE_BLOCK\n", replacement))


def untouched_newer_formulae(project, tag, before, after):
    requested = version_key(project, f"{tag}.tar.gz")
    return {
        path for path, content in after.items()
        if before.get(path) == content and version_key(project, formula_source(content)[0]) > requested
    }


def verify_formulae(project, tag, phase, before, after, changed, fetch=load_json,
                    read_template=load_text, digest_asset=asset_digest):
    paths = project_paths(project, tag)
    if not changed or not changed <= paths:
        raise ValueError("release PR changes paths outside its formula channel")
    paths -= untouched_newer_formulae(project, tag, before, after)
    if not paths:
        return
    expected_filename, checksum = source_digest(project, tag, fetch)
    bottles = release_bottles(project, tag, fetch, digest_asset) if phase == "bottles" else {}
    release_url = f"{FORGE}/{OWNER}/{project}/releases/download/{tag}"

    for path in sorted(paths):
        content = after[path]
        url, digest = formula_source(content)
        address = urllib.parse.urlsplit(url)
        if (
            address.scheme != "https" or address.netloc != "files.pythonhosted.org"
            or PurePosixPath(address.path).name != expected_filename or digest != checksum
        ):
            raise ValueError(f"{path} does not match the published source archive")
        prior = formula_source(before[path]) if path in before else None
        if prior and version_key(project, prior[0]) > version_key(project, url):
            raise ValueError(f"{path} would replace a newer release")

        block = bottle_block(content)
        template_url = f"{FORGE}/{OWNER}/{project}/raw/tag/{tag}/packaging/homebrew/{PurePosixPath(path).name}"
        template = read_template(template_url)
        if phase == "formula":
            if block:
                raise ValueError(f"{path} adds bottles in the source-formula phase")
        else:
            prior_block = bottle_block(before[path]) if path in before else ""
            if prior != (url, digest) or before[path] != render_template(template, tag, digest, prior_block):
                raise ValueError(f"{path} needs the matching source formula on main first")
            lines = block.splitlines()
            if len(lines) != 4 or lines[0] != f'    root_url "{release_url}"':
                raise ValueError(f"{path} does not point at the three bottles from {tag}")
            rendered = {}
            for line in lines[1:]:
                match = re.fullmatch(rf'    sha256 cellar: (:[a-z_]+|"[^"]+"), (\w+): +"({HASH})"', line)
                if match is None:
                    raise ValueError(f"{path} has an unexpected bottle declaration")
                cellar, platform, bottle_sha = match.groups()
                rendered[platform] = (bottle_sha, cellar[1:] if cellar.startswith(":") else json.loads(cellar))
            expected = bottles.get(f"sisyphusmd/tap/{PurePosixPath(path).stem}")
            if rendered != expected or set(rendered) != PLATFORMS:
                raise ValueError(f"{path} bottle checksums do not match the published manifests")
        if content != render_template(template, tag, digest, block):
            raise ValueError(f"{path} does not match the tagged formula template")


def run(ref, base, head):
    match = REF.fullmatch(ref)
    if match is None or match[1] not in PROJECTS or not all(SHA.fullmatch(sha) for sha in (base, head)):
        raise ValueError("invalid generated release branch or commit")
    project, tag, phase = match.groups()
    paths = project_paths(project, tag)
    changed = set(git("diff", "--no-renames", "--name-only", base, head).splitlines())
    before = {}
    after = {}
    for path in paths:
        if git("ls-tree", base, "--", path):
            before[path] = subprocess.check_output(["git", "show", f"{base}:{path}"]).decode("utf-8")
        entry = git("ls-tree", head, "--", path)
        if not entry.startswith("100644 blob "):
            raise ValueError(f"{path} must be a regular formula")
        after[path] = subprocess.check_output(["git", "show", f"{head}:{path}"]).decode("utf-8")
    verify_formulae(project, tag, phase, before, after, changed)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            raise ValueError("usage: check-release-formulae.py BRANCH BASE_SHA HEAD_SHA")
        run(*sys.argv[1:])
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Cannot verify tap release: {exc}")
