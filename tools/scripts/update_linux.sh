#!/bin/sh

# Check if no arguments are provided, try to read from build-config.json
if [ -z "$1" ] && [ -z "$2" ]; then
  release_branch_path=$(jq -r '.["release-branch-path"] // empty' build-config.json 2>/dev/null)
fi

# Check if release_branch_path is provided (either as an argument or from build-config.json)
if [ -z "$release_branch_path" ] &&  [ -z "$1" ]; then
    # If build-config.json is present but didn't have release-branch-path, or if we are just running in the root
    if [ -f "build-config.json" ]; then
        release_branch_path="."
    else
        echo "Error: Missing release_branch_path."
        echo "Usage: $0 <release_branch_path> <major_version>"
        echo "Example: $0 /path/to/release/branch 6.1"
        exit 1
    fi
else
  if [ -n "$1" ]; then
    release_branch_path=$1
  fi
fi

# Check if major_version is provided
if [ -z "$2" ]; then
  # If major_version is not provided, extract the list of available versions from the spec files in the release branch path
  # Only match directories starting with v followed by a number
  major_versions=$(find SPECS/linux/ -mindepth 1 -maxdepth 1 -type d -name "v[0-9]*" | sed -E 's/.*\/v([0-9]+\.[0-9]+)/\1/' | sort -u)

  if [ -z "$major_versions" ]; then
    if [ -f "SPECS/linux/linux.spec" ]; then
       major_versions=$(grep "^Version:" SPECS/linux/linux.spec | awk '{print $2}' | cut -d. -f1-2)
    fi
  fi

  if [ -z "$major_versions" ]; then
    echo "Error: No major versions found in SPECS/linux/."
    exit 1
  fi

  echo "Available major versions:"
  echo "$major_versions"
else
  major_versions=$2
fi

# Loop over major_versions if no major_version argument is provided
for major_version in $major_versions; do
  # Update the specs with the provided major version
  if [ -d "SPECS/linux/v${major_version}" ]; then
    specs=$(find SPECS/linux/v${major_version} -name "*.spec")
  else
    specs=$(find SPECS/linux/ -maxdepth 1 -name "*.spec")
  fi

  # Fetch the latest tarball URL based on the major version input
  tarball_url=$(curl -s https://www.kernel.org | grep -Eo "https://cdn.kernel.org/pub/linux/kernel/v${major_version%%.*}.x/linux-${major_version}\.[0-9]*.tar.xz" | uniq)
  tarball=$(basename $tarball_url)
  version=$(echo $tarball | sed 's/linux-//; s/.tar.xz//')
  echo "Latest Linux version for $major_version: $version"

  # Check if the tarball already exists, exit if up to date
  if test -f ${release_branch_path}/stage/SOURCES/$tarball; then
    echo "Up to date for $major_version"
    continue
  fi

  # Download the tarball if not up to date
  $(cd ${release_branch_path}/stage/SOURCES && wget $tarball_url)

  # Calculate the sha512 checksum of the tarball
  sha512=$(sha512sum ${release_branch_path}/stage/SOURCES/$tarball | awk '{print $1}')

  # Create the changelog entry
  changelog_entry=$(echo "`date +"%a %b %d %Y"` `git config user.name` <`git config user.email`> $version-1")

  # Update the spec files
  for spec in $specs; do
    sed -i "/^Version:/ s/${major_version}.[0-9]*/$version/" $spec
    sed -i '/^Release:/ s/[0-9]*%/1%/' $spec
    sed -i "/^%define sha512 linux/ s/=[0-9a-f]*$/=$sha512/" $spec
    sed -i "/^%changelog/a* $changelog_entry\n- Update to version $version" $spec
  done

  for spec in $specs; do
    config_yaml_file="$(dirname ${spec})/config.yaml"
    break
  done

  # Update the archive source by matching the linux-$major_version pattern in config.yaml
  if [ -f "$config_yaml_file" ]; then
    # Update the config.yaml using jq to target the archive source
    echo "Getting the commit id for linux-$version"

    tmp_dir=$(mktemp -d)
    git clone --depth 1 --branch linux-$major_version.y https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git "$tmp_dir"
    pushd "$tmp_dir"
    commit_id="$(git rev-parse HEAD)"
    popd
    rm -rf "$tmp_dir"

    # Use inline python with ruamel.yaml to preserve formatting and comments
    # Note: yq is not available in Photon
    python3 -c "
import re
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

with open(\"$config_yaml_file\", 'r') as f:
    data = yaml.load(f)

pattern = re.compile(r'^linux-${major_version}\.[0-9]+')
for source in data.get('sources', []):
    if pattern.match(source.get('archive', '')):
        source['commit_id'] = \"$commit_id\"
        source['archive_sha512sum'] = \"$sha512\"
        break

with open(\"$config_yaml_file\", 'w') as f:
    yaml.dump(data, f)
"

  # Need to escape the dot in the major version
  m_ver=$(cut -d '.' -f 1 <<< "$major_version")
  min_ver=$(cut -d '.' -f 2 <<< "$major_version")
  sed -i -E "/fips-canister/! s/$m_ver\.$min_ver\.[0-9]+/$version/g" "$config_yaml_file"

  fi
done