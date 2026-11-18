"""Submit rendered formulae from an isolated job. Wait for main separately."""

import json
import os
import runpy
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
validation = runpy.run_path(str(DIRECTORY / "check-release-formulae.py"))
FORGE = validation["FORGE"]
REPO = "SisyphusMD/homebrew-tap"
API = f"{FORGE}/api/v1/repos/{REPO}"


def git(*args, env=None):
    return subprocess.check_output(["git", *args], text=True, env=env).strip()


def api(path, token, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        API + path, data=data, headers={"Authorization": f"token {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def current_values(commit, paths):
    return {
        path: subprocess.check_output(["git", "show", f"{commit}:{path}"])
        for path in paths if git("ls-tree", commit, "--", path)
    }


def read_artifact(directory, paths):
    files = {}
    for path in paths:
        source = directory / path
        if not source.is_file() or source.is_symlink() or source.stat().st_size > 100_000:
            raise ValueError(f"invalid formula artifact {path}")
        files[path] = source.read_bytes()
    if {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()} != paths:
        raise ValueError("unexpected files in the formula artifact")
    return files


def candidate_commit(base, parent, rendered, message):
    with tempfile.TemporaryDirectory() as scratch:
        index_env = dict(os.environ, GIT_INDEX_FILE=str(Path(scratch) / "index"))
        git("read-tree", base, env=index_env)
        for path, content in sorted(rendered.items()):
            blob = subprocess.check_output(["git", "hash-object", "-w", "--stdin"], input=content)
            git("update-index", "--add", "--cacheinfo", f"100644,{blob.decode().strip()},{path}", env=index_env)
        tree = git("write-tree", env=index_env)
    current_base = subprocess.run(["git", "merge-base", "--is-ancestor", base, parent], check=False)
    if current_base.returncode not in (0, 1):
        current_base.check_returncode()
    if not current_base.returncode and tree == git("rev-parse", f"{parent}^{{tree}}"):
        return parent
    parents = ["-p", parent]
    if current_base.returncode:
        parents += ["-p", base]
    return git(
        "-c", "user.name=forgejo-actions[bot]",
        "-c", "user.email=forgejo-actions[bot]@users.noreply.bryantserver.com",
        "commit-tree", tree, *parents, "-m", message,
    )


def submit(project, tag, phase, artifact, token, git_env, request=api):
    branch = f"tap/{project}/{tag}/{phase}"
    if project not in validation["PROJECTS"] or not validation["REF"].fullmatch(branch):
        raise ValueError("invalid source project, tag or phase")
    if (Path.cwd() != Path(git("rev-parse", "--show-toplevel"))
        or git("remote", "get-url", "origin") != f"{FORGE}/{REPO}.git" or git("status", "--porcelain")):
        raise ValueError("use a clean checkout of Forgejo's primary tap")
    paths = validation["project_paths"](project, tag)
    rendered = read_artifact(artifact, paths)
    git("fetch", "--no-tags", "origin", "refs/heads/main:refs/remotes/origin/main")
    base = git("rev-parse", "origin/main")
    if current_values(base, paths) == rendered:
        texts = {path: content.decode("utf-8") for path, content in rendered.items()}
        landed_phase = "bottles" if all(validation["bottle_block"](text) for text in texts.values()) else phase
        validation["verify_formulae"](project, tag, landed_phase, texts, texts, paths)
        return {"state": "landed"}

    key = urllib.parse.urlencode({"state": "all", "head": branch, "page": 1, "limit": 50})
    known = [
        pr for pr in request(f"/pulls?{key}", token)
        if pr["head"]["label"] == branch and (pr["head"].get("repo") or {}).get("full_name") == REPO
        and pr["base"]["ref"] == "main"
    ]
    if any(pr["state"] == "closed" and not pr["merged"] for pr in known):
        raise ValueError("the existing pull request closed before this artifact landed")
    known = [pr for pr in known if pr["state"] == "open"]
    if len(known) > 1:
        raise ValueError("multiple open pull requests for the formula branch")

    full_ref = f"refs/heads/{branch}"
    advertised = any(line.endswith(f"\t{full_ref}") for line in git("ls-remote", "origin", full_ref).splitlines())
    if advertised:
        git("fetch", "--no-tags", "origin", full_ref)
        parent = git("rev-parse", "FETCH_HEAD")
    else:
        parent = base
    candidate = candidate_commit(base, parent, rendered, f"chore: update {project} {phase} (publish {tag})")
    validation["run"](branch, base, candidate)
    if not advertised or candidate != parent:
        git("push", "origin", f"{candidate}:{full_ref}", env=git_env)
    if known:
        return {"state": "pending", "url": known[0]["html_url"]}

    body = (
        "Refs #6.\n\n"
        f"Source: {FORGE}/SisyphusMD/{project}/releases/tag/{tag}\n"
        f"Phase: {phase}.\n\n"
        "No tests: Published package metadata and formula syntax are checked in this pull request."
    )
    pr = request("/pulls", token, {
        "head": branch, "base": "main", "body": body,
        "title": f"Update {project} {phase} for {tag}",
    })
    if pr["head"]["sha"] != candidate:
        raise ValueError("Forgejo did not open the prepared formula commit")
    return {"state": "pending", "url": pr["html_url"]}


if __name__ == "__main__":
    import base64
    try:
        if len(sys.argv) != 5:
            raise ValueError("usage: open-release-formula-pr.py PROJECT TAG PHASE ARTIFACT_DIRECTORY")
        token = os.environ.pop("TOKEN")
        if not token:
            raise ValueError("missing tap repository token")
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        git_env = dict(os.environ, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="http.extraheader",
                       GIT_CONFIG_VALUE_0=f"Authorization: Basic {basic}")
        print(json.dumps(submit(*sys.argv[1:4], Path(sys.argv[4]), token, git_env)))
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Cannot submit tap release: {exc}")
