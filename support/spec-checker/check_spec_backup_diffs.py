#!/usr/bin/env python3
"""
Generic validator: given two rev:path specs (old main vs new backup), verify
the unified diff contains only allowed added/removed line patterns from config.

Used by the pre-push hook for SPECS/<subrelease>/<pkg>/<name>.spec backups.

Modes:
  - Pass old_rev_path and new_rev_path explicitly (with --subrelease).
  - Or pass --commit COMMIT: discover (old_rev_path, new_rev_path) from
    "git diff --name-status --diff-filter=AR -M COMMIT^ COMMIT" (and M for
    modified paths); for each added/renamed SPECS/<N>/<pkg>/<name>.spec where
    SPECS/<pkg>/<name>.spec was modified, run the check.
"""

import json
import re
import subprocess
import sys
from pathlib import Path


def get_repo_root():
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL
        )
        return Path(output.decode().strip())
    except subprocess.CalledProcessError:
        raise RuntimeError("Not inside a Git repository")


REPO_ROOT = get_repo_root()

RULES_DIR = Path(__file__).resolve().parent
DEFAULT_RULES_PATH = RULES_DIR / "spec-backup-diff-rules.json"
BACKUP_SPEC_RE = re.compile(r"^SPECS/(\d+)/([^/]+)/([^/]+\.spec)$")


def _spec_name_from_rev_path(rev_path):
    """Extract spec/package name from rev:path e.g. 'COMMIT:SPECS/91/sendmail/sendmail.spec' -> 'sendmail'."""
    if ":" not in rev_path:
        return ""
    path = rev_path.split(":", 1)[1]
    parts = path.split("/")
    # SPECS/<subrelease>/<pkg>/<name>.spec -> pkg at index 2
    return parts[2] if len(parts) > 2 else ""


def _load_rules_data(rules_path):
    """Load rules from JSON file. Raises SystemExit on missing file or invalid JSON."""
    if not rules_path.exists():
        raise SystemExit(f"Rules file not found: {rules_path}")
    if rules_path.suffix != ".json":
        raise SystemExit(f"Rules file must be JSON: {rules_path}")
    try:
        with open(rules_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {rules_path}: {e}") from e
    if not isinstance(data, dict):
        raise SystemExit(f"Rules file must be a JSON object: {rules_path}")
    return data


def load_rules(rules_path, subrelease):
    data = _load_rules_data(rules_path)
    added = data.get("allowed_added")
    removed = data.get("allowed_removed")
    if not isinstance(added, list):
        added = []
    if not isinstance(removed, list):
        removed = []
    sub = str(subrelease)

    def compile_line(pat, kind, i):
        if not isinstance(pat, str):
            raise SystemExit(f"Rules file: {kind}[{i}] must be a string, got {type(pat).__name__}")
        try:
            return re.compile(pat.replace("{subrelease}", sub))
        except re.error as e:
            raise SystemExit(f"Rules file: invalid regex in {kind}[{i}] {pat!r}: {e}") from e

    return (
        [compile_line(p, "allowed_added", i) for i, p in enumerate(added)],
        [compile_line(p, "allowed_removed", i) for i, p in enumerate(removed)],
    )


_RULES_CACHE = {}  # (rules_path, subrelease) -> (allowed_added, allowed_removed)


def get_rules_cached(rules_path, subrelease):
    key = (rules_path, str(subrelease))
    if key not in _RULES_CACHE:
        _RULES_CACHE[key] = load_rules(rules_path, subrelease)
    return _RULES_CACHE[key]


def run_git_diff(repo_root, old_rev_path, new_rev_path):
    """Run git diff between two rev:path blobs; return unified diff (one subprocess)."""
    result = subprocess.run(
        ["git", "diff", "--no-color", old_rev_path, new_rev_path],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"git diff failed: {result.stderr}")
    return result.stdout


def check_diff(
    repo_root,
    old_rev_path,
    new_rev_path,
    allowed_added,
    allowed_removed
):
    """Compare old vs new file via one git diff; return list of (kind, line) for disallowed changes."""
    diff_out = run_git_diff(repo_root, old_rev_path, new_rev_path)
    disallowed = []
    for raw in diff_out.splitlines(keepends=True):
        if not raw.startswith("+") and not raw.startswith("-"):
            continue
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        content = (raw[1:].rstrip("\n") if len(raw) > 1 else "")
        if raw.startswith("+"):
            if any(p.match(content) for p in allowed_added):
                continue
            disallowed.append(("added", raw.rstrip("\n")))
        elif raw.startswith("-"):
            if any(p.match(content) for p in allowed_removed):
                continue
            disallowed.append(("removed", raw.rstrip("\n")))
    return disallowed


def _name_status_and_modified(repo_root, commit):
    """
    Single git diff --name-status -M commit^ commit.
    Returns (list of (status, path1, path2), set of modified path1).
    Returns ([], set()) if commit has no parent or git fails.
    """
    r = subprocess.run(
        ["git", "diff", "--name-status", "-M", f"{commit}^", commit],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if r.returncode:
        return [], set()
    added_renamed = []
    modified_paths = set()
    for line in r.stdout.strip().splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = (parts[0][0] if parts[0] else "")
        path1 = parts[1]
        path2 = parts[2] if len(parts) > 2 else None
        if status in "AR":
            added_renamed.append((status, path1, path2))
        elif status == "M":
            modified_paths.add(path1)
    return added_renamed, modified_paths


def pairs_from_diff_filter(repo_root, commit):
    """
    Get (old_rev_path, new_rev_path, subrelease) for each spec-backup pair in commit
    using git diff --name-status -M (one call), then filter to AR + M in Python.
    """
    added_renamed, modified_paths = _name_status_and_modified(repo_root, commit)

    pairs = []
    for status, path1, path2 in added_renamed:
        if status == "A":
            m = BACKUP_SPEC_RE.match(path1)
            if not m:
                continue
            subrelease, pkg, name = m.group(1), m.group(2), m.group(3)
            main_path = f"SPECS/{pkg}/{name}"
            if main_path not in modified_paths:
                continue
            old_rev_path = f"{commit}^:{main_path}"
            new_rev_path = f"{commit}:{path1}"
            pairs.append((old_rev_path, new_rev_path, subrelease))
        elif status == "R" and path2:
            m = BACKUP_SPEC_RE.match(path2)
            if not m:
                continue
            subrelease = m.group(1)
            # Rename: main spec (path1) was renamed to backup (path2). No need to
            # require path1 in modified_paths — renames are reported as R, not M.
            old_rev_path = f"{commit}^:{path1}"
            new_rev_path = f"{commit}:{path2}"
            pairs.append((old_rev_path, new_rev_path, subrelease))
    return pairs


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Check spec backup diff against allowed rules")
    ap.add_argument("old_rev_path", nargs="?", help="e.g. abc123^:SPECS/sendmail/sendmail.spec")
    ap.add_argument("new_rev_path", nargs="?", help="e.g. abc123:SPECS/91/sendmail/sendmail.spec")
    ap.add_argument("--commit", metavar="COMMIT", default="HEAD", help="Discover old/new rev paths from git diff --diff-filter=AR (default: HEAD)")
    ap.add_argument("--subrelease", help="e.g. 91 (required when passing old_rev_path/new_rev_path)")
    ap.add_argument("--rules", type=Path, default=None, help="Path to spec-backup-diff-rules.json (default: githooks/spec-backup-diff-rules.json)")
    ap.add_argument("--repo", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    if args.rules is None:
        args.rules = DEFAULT_RULES_PATH
    elif not args.rules.is_absolute():
        args.rules = (args.repo / args.rules).resolve()

    repo = args.repo
    if not repo.is_dir():
        raise SystemExit(f"Repo path is not a directory: {repo}")

    errors = []

    explicit_mode = args.old_rev_path and args.new_rev_path and args.subrelease
    if not explicit_mode:
        for old_rev_path, new_rev_path, subrelease in pairs_from_diff_filter(repo, args.commit):
            try:
                allowed_added, allowed_removed = get_rules_cached(args.rules, subrelease)
                disallowed = check_diff(repo, old_rev_path, new_rev_path, allowed_added, allowed_removed)
            except RuntimeError as e:
                errors.append(f"{old_rev_path} vs {new_rev_path}: {e}\n")
                continue
            if disallowed:
                errors.append(f"{old_rev_path} vs {new_rev_path}:\n")
                for kind, line in disallowed:
                    errors.append(f"  {kind}: {line!r}\n")
            else:
                spec_name = _spec_name_from_rev_path(new_rev_path)
                if spec_name:
                    print(f"OK: {spec_name}")
        if errors:
            print("spec-backup diff validation failed:\n", file=sys.stderr)
            for e in errors:
                if ".spec" in e:
                    print("")
                sys.stderr.write(e)
            sys.exit(1)
        sys.exit(0)
    else:
        if not args.old_rev_path or not args.new_rev_path or not args.subrelease:
            ap.error("old_rev_path, new_rev_path, and --subrelease are required for explicit mode")
        try:
            allowed_added, allowed_removed = load_rules(args.rules, args.subrelease)
            disallowed = check_diff(
                repo,
                args.old_rev_path,
                args.new_rev_path,
                allowed_added,
                allowed_removed,
            )
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        if disallowed:
            for kind, line in disallowed:
                print(f"  {kind}: {line!r}", file=sys.stderr)
            sys.exit(1)
        spec_name = _spec_name_from_rev_path(args.new_rev_path)
        if spec_name:
            print(f"OK: {spec_name}")
        sys.exit(0)


if __name__ == "__main__":
    main()
