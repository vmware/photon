#!/usr/bin/env python3
#
# Update Linux kernel spec files and config.yaml to the latest stable version.
#
# Usage: update_linux.py -s SPEC_DIR [OPTIONS]
#
# Options:
#   -s, --spec-dir             Path to the spec directory containing kernel spec
#                              files (required). The major version is extracted
#                              from the Version field in the spec files.
#
#   -r, --release-branch-path  Path to the release branch root. If omitted, the
#                              script reads "release-branch-path" from
#                              build-config.json in the current directory.
#                              This is basically just used to store the downloaded
#                              tarball for subsequent builds.
#
#   -l, --linux-repo           Path to an existing local clone of the stable
#                              Linux repository. If provided, the script uses it
#                              instead of cloning a fresh copy.
#
#   -c, --commit               Auto-commit changes. Without this flag, the
#                              commit message is saved to commit-msg.txt.
#
# The script:
#   1. Queries kernel.org JSON API for the latest stable tarball URL.
#   2. Skips if the spec files already declare that version.
#   3. Downloads the tarball, verifies SHA-256, and computes SHA-512 checksum.
#   4. Updates Version, Release, sha512, and %changelog in all matching .spec files.
#   5. Updates commit_id, archive_sha512sum, and version strings in config.yaml
#      (preserving YAML formatting/comments via ruamel.yaml).
#   6. Optionally commits the changes with a message listing any dropped patches.

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import os
import requests

from datetime import datetime
from hashlib import sha256, sha512
from pathlib import Path
from shutil import rmtree

from ruamel.yaml import YAML

KERNEL_RELEASE_JSON_URL = "https://www.kernel.org/releases.json"
STABLE_REPO = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git"


def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


class Git:
    def __init__(self, repo=None):
        self.repo = repo

    def _run(self, *args, capture=False):
        cmd = ["git", *args]
        result = subprocess.run(
            cmd,
            cwd=self.repo,
            text=True,
            capture_output=capture
        )
        if result.returncode:
            if result.stdout:
                print(f"STDOUT: {result.stdout}")
            die("STDERR: " + result.stderr.strip() if result.stderr else "Unknown error")
        return result.stdout.strip() if capture else ""

    def run(self, *args):
        self._run(*args)

    def output(self, *args):
        return self._run(*args, capture=True)

    def try_output(self, *args):
        cmd = ["git", *args]
        result = subprocess.run(
            cmd,
            cwd=self.repo,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            return None
        return result.stdout.strip()

    def add(self, path):
        self.run("add", "-A", path)

    def commit(self, msg):
        self.run("commit", "-m", msg)

    def status(self):
        return self.output("status", "--porcelain")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Update Linux kernel spec files to the latest stable version."
    )
    parser.add_argument(
        "-s", "--spec-dir",
        type=Path,
        required=True,
        help="Path to the spec directory containing kernel spec files (required)",
    )
    parser.add_argument(
        "-r", "--release-branch-path",
        type=Path,
        default=None,
        help="Path to the release branch (default: from build-config.json or '.')",
    )
    parser.add_argument(
        "-l", "--linux-repo",
        type=Path,
        default=None,
        help="Path to an existing local linux-stable clone (avoids re-cloning)",
    )
    parser.add_argument(
        "-c", "--commit",
        action="store_true",
        help="Auto-commit changes (default: save commit message to commit-msg.txt)",
    )
    return parser.parse_args()


def resolve_release_branch_path(arg_path):
    if arg_path:
        return arg_path

    # First try to read from build-config.json
    try:
        config = json.loads(Path("build-config.json").read_text())
        path = config.get("release-branch-path")
        if path:
            return Path(path)
    except FileNotFoundError:
        die("Missing release_branch_path - build-config.json not found.")
    except json.JSONDecodeError:
        die("Failed to decode build-config.json")

    # If nothing in build-config.json, check if we have a stage directory
    cwd = os.getcwd()
    if os.path.exists(f"{cwd}/stage") and os.path.exists("build-config.json"):
        return Path(cwd)

    die(
        "release_branch_path not specified in build-config.json and no local stage/ directory. " +
        "If you are in common branch, please specify with --release-branch-path, " +
        "create a local stage/, or specify in build-config.json"
    )


def find_specs(spec_dir):
    specs = sorted(spec_dir.glob("*.spec"))
    if not specs:
        die(f"No .spec files found in {spec_dir}")
    return specs


def extract_major_version(specs):
    for spec in specs:
        for line in spec.read_text().splitlines():
            match = re.match(r"^Version:\s+(\d+\.\d+)\.\d+", line)
            if match:
                return match.group(1)
    die(f"Could not determine major version from spec files: {[str(s) for s in specs]}")


def spec_has_version(specs, version):
    pattern = re.compile(rf"^Version:\s*{re.escape(version)}\s*$", re.MULTILINE)
    return any(pattern.search(spec.read_text()) for spec in specs)


def fetch_latest_tarball_url(major_version):
    raw_json = urllib.request.urlopen(KERNEL_RELEASE_JSON_URL, timeout=30).read().decode()
    release_json = json.loads(raw_json)

    for release in release_json['releases']:
        release_maj_ver = '.'.join(release['version'].split('.')[0:2])
        if release_maj_ver == major_version:
            return release['source']

    return None


def compute_hash(filepath, algorithm):
    h = algorithm()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_tarball_sha256(tarball_path, major_version):
    major_x = major_version.split(".")[0]
    sha256sums_url = f"https://www.kernel.org/pub/linux/kernel/v{major_x}.x/sha256sums.asc"
    try:
        response = urllib.request.urlopen(sha256sums_url, timeout=30)
        sha256sums = response.read().decode()
    except Exception as e:
        die(f"Could not fetch SHA256 checksums from kernel.org: {e}")

    tarball_name = os.path.basename(str(tarball_path))
    local_sha256 = compute_hash(tarball_path, sha256)

    for line in sha256sums.splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[1] == tarball_name:
            if parts[0] == local_sha256:
                print(f"SHA256 verification passed for {tarball_name}")
                return True
            else:
                die(f"SHA256 mismatch for {tarball_name}: expected {parts[0]}, got {local_sha256}")

    die(f"{tarball_name} not found in kernel.org sha256sums.asc")


def build_changelog_entry(photon_git, version):
    date_str = datetime.now().strftime("%a %b %d %Y")
    name = photon_git.output("config", "user.name")
    email = photon_git.output("config", "user.email")
    return f"{date_str} {name} <{email}> {version}-1"


# Assumes that linux_git is checked out to the correct branch
def drop_upstreamed_patches(spec, linux_git):
    dropped_patches = []
    for root, dirs, files in os.walk(spec.parent):
        for file in files:
            if not file.endswith(".patch"):
                continue

            # Try to extract the upstream commit hash
            with open(os.path.join(root, file)) as f:
                for line in f:
                    match = re.match(r"commit\s+([0-9a-fA-F]+)\s+upstream", line, re.IGNORECASE)
                    match1 = re.match(r"\[\s*Upstream\s+commit\s+([0-9a-fA-F]+)\s*\]", line,
                                        re.IGNORECASE)
                    if not match and not match1:
                        continue

                    commit_hash = match.group(1) if match else match1.group(1)
                    if not commit_hash:
                        continue

                    search_pattern = rf"\[\s*Upstream\s+commit\s+{commit_hash}\s*\]"
                    search_pattern1 = rf"commit\s+{commit_hash}\s+upstream"

                    result = None
                    try:
                        result = linux_git.try_output(
                            "log", "-E", "-i", f"--grep={search_pattern}",
                            f"--grep={search_pattern1}", "-1", "--oneline", "--since=2 months ago",
                        )
                    except Exception as e:
                        print(f"Error checking for backported patch {commit_hash}: {e}")
                        break

                    if not result:
                        break

                    downstream_hash = result.split()[0]

                    os.remove(os.path.join(root, file))
                    dropped_patches.append((commit_hash, downstream_hash, os.path.join(root, file)))

                    print(
                            f"Found upstream patch {commit_hash} backported as commit "
                            +f"{downstream_hash[:12]} - dropping patch file "
                            + f"{os.path.basename(file)}"
                        )

    return dropped_patches


def update_spec_files(photon_git, linux_git, specs, major_version, version, sha512_hash):
    changelog_entry = build_changelog_entry(photon_git, version)

    print(f"Using Linux repository at {linux_git.repo} to check for backported patches")
    linux_git.run("checkout", f"linux-{major_version}.y")
    print(f"Pulling latest changes from origin for linux-{major_version}.y")
    linux_git.run("pull", "origin", f"linux-{major_version}.y", "--rebase")
    dropped_patches = drop_upstreamed_patches(specs[0], linux_git)

    # Lambdas avoid re.sub interpreting dynamic values as backreferences
    replacements = [
        (
            rf"^(Version:\s*){re.escape(major_version)}\.\d+",
            lambda m: m.group(1) + version,
        ),
        (
            r"^(Release:\s*)\d+(%)",
            lambda m: m.group(1) + "1" + m.group(2),
        ),
        (
            r"^(%define\s+sha512\s+linux\s*=)[0-9a-f]*$",
            lambda m: m.group(1) + sha512_hash,
        ),
        (
            r"^(%changelog)",
            lambda m: f"%changelog\n* {changelog_entry}\n- Update to version {version}",
        ),
    ]

    if dropped_patches:
        print(f"Dropping {len(dropped_patches)} upstreamed patches for {major_version}")
        for patch in dropped_patches:
            replacements.extend([
                (
                    rf"^\#.*\nPatch[0-9]+:\s+({re.escape(os.path.basename(patch[2]))})\n+",
                    "",
                ),
                (
                    rf"^Patch[0-9]+:\s+({re.escape(os.path.basename(patch[2]))})\n+",
                    ""
                )
            ])

    for spec in specs:
        content = spec.read_text()
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        spec.write_text(content)

    return dropped_patches

def get_stable_commit_id(linux_git, major_version):
    linux_git.run("checkout", f"linux-{major_version}.y")
    return linux_git.output("rev-parse", "HEAD")


def update_config_yaml(linux_git, specs, major_version, version, sha512_hash):
    if not specs:
        return

    config_path = specs[0].parent / "config.yaml"
    if not config_path.is_file():
        return

    print(f"Getting the commit id for linux-{version}")
    commit_id = get_stable_commit_id(linux_git, major_version)

    yaml = YAML()
    yaml.preserve_quotes = True

    data = yaml.load(config_path)
    archive_pattern = re.compile(rf"^linux-{re.escape(major_version)}\.\d+")
    for source in data.get("sources", []):
        if archive_pattern.match(source.get("archive", "")):
            source["commit_id"] = commit_id
            source["archive_sha512sum"] = sha512_hash
            break
    with open(config_path, "w") as f:
        yaml.dump(data, f)

    # Replace version strings on lines not related to fips-canister
    ver_pattern = re.compile(rf"{re.escape(major_version)}\.\d+")
    lines = config_path.read_text().splitlines(keepends=True)
    with open(config_path, "w") as f:
        for line in lines:
            if "fips-canister" not in line:
                line = ver_pattern.sub(version, line)
            f.write(line)


def clone_stable_repo(photon_git, major_version, path):
    if os.path.exists(path):
        return

    try:
        photon_git.run("clone", "--branch", f"linux-{major_version}.y",
            STABLE_REPO, str(path))
    except Exception:
        die(f"Failed to clone stable repository for {major_version} to {path}")


def build_commit_message(version, dropped_patches):
    lines = [f"linux: update to {version}"]
    if dropped_patches:
        lines.append("")
        lines.append("Dropped upstreamed patches:")
        for upstream_hash, downstream_hash, patch_file in dropped_patches:
            name = os.path.basename(patch_file)
            lines.append(f"- {name}\n\tupstream: {upstream_hash[:12]}\n\tbackported: {downstream_hash[:12]}")
    return "\n".join(lines)


def commit_update(photon_git, spec_dir, version, dropped_patches, commit=False):
    if commit:
        photon_git.add(str(spec_dir))

        if not photon_git.status():
            print("No changes to commit")
            return

    message = build_commit_message(version, dropped_patches)
    if not commit:
        msg_path = Path("commit-msg.txt").resolve()
        msg_path.write_text(message)
        print(f"Drafted commit message saved to {msg_path}. Please review and commit manually.")
        print(f"Commit message:\n{message}")
        return

    photon_git.commit(message)
    print(f"Committed: {message.splitlines()[0]}")


def main():
    args = parse_args()
    spec_dir = args.spec_dir.resolve()
    if not spec_dir.is_dir():
        die(f"{spec_dir} is not a valid directory!")

    specs = find_specs(spec_dir)
    major_version = extract_major_version(specs)
    print(f"Detected major version {major_version} from spec files in {spec_dir}")

    release_branch_path = resolve_release_branch_path(args.release_branch_path)
    tmp_repo = release_branch_path / "stage" / "SOURCES" / "linux-tmp-repo"
    download_in_progress = False

    photon_git = Git(repo=spec_dir)
    repo_root = photon_git.output("rev-parse", "--show-toplevel")
    photon_git = Git(repo=repo_root)

    if not os.path.exists(tmp_repo.parent):
        os.makedirs(tmp_repo.parent)

    linux_repo_path = args.linux_repo
    if not linux_repo_path:
        clone_stable_repo(photon_git, major_version, tmp_repo)
        linux_repo_path = tmp_repo
    linux_git = Git(repo=linux_repo_path)

    try:
        tarball_url = fetch_latest_tarball_url(major_version)
        if not tarball_url:
            die(f"Could not find tarball URL for {major_version}")

        tarball = Path(tarball_url).name
        version = tarball.removeprefix("linux-").removesuffix(".tar.xz")
        print(f"Latest Linux version for {major_version}: {version}")

        if spec_has_version(specs, version):
            print(f"Up to date for {major_version}")
            return

        tarball_path = release_branch_path / "stage" / "SOURCES" / tarball

        retries = 2
        while retries >= 0:
            if not os.path.exists(tarball_path):
                print(f"Downloading {tarball_url}")
                download_in_progress = True
                response = requests.get(tarball_url, stream=True, timeout=500)
                response.raise_for_status()
                with open(tarball_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                download_in_progress = False

            if not verify_tarball_sha256(tarball_path, major_version):
                os.remove(tarball_path)
                if retries == 0:
                    die(f"SHA256 verification failed for {tarball_path}, removed corrupted file")
            else:
                break

            retries -= 1

        sha512_hash = compute_hash(tarball_path, sha512)

        dropped_patches = update_spec_files(
            photon_git, linux_git, specs, major_version, version, sha512_hash,
        )
        update_config_yaml(
            linux_git, specs, major_version, version, sha512_hash,
        )
        commit_update(photon_git, spec_dir, version, dropped_patches, commit=args.commit)
    finally:
        if os.path.exists(tmp_repo):
            rmtree(tmp_repo)

        if download_in_progress:
            os.remove(tarball_path)

if __name__ == "__main__":
    main()
