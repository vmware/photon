#!/bin/sh

# Check if no arguments are provided, try to read from build-config.json
if [ -z "$1" ] && [ -z "$2" ]; then
  release_branch_path=$(jq -r '.["release-branch-path"]' build-config.json)
fi

# Check if release_branch_path is provided (either as an argument or from build-config.json)
if [ -z "$release_branch_path" ] &&  [ -z "$1" ]; then
  echo "Error: Missing release_branch_path."
  echo "Usage: $0 <release_branch_path> <major_version>"
  echo "Example: $0 /path/to/release/branch 6.1"
  exit 1
else
  if [ -n "$1" ]; then
    release_branch_path=$1
  fi
fi

# Check if major_version is provided
if [ -z "$2" ]; then
  # If major_version is not provided, extract the list of available versions from the spec files in the release branch path
  major_versions=$(find SPECS/linux/ -mindepth 1 -maxdepth 1 -type d -name "v*" | sed -E 's/.*\/v([0-9]+\.[0-9]+)/\1/' | sort -u)

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
  specs=$(find SPECS/linux/v${major_version} -name "*.spec")

  # Fetch the latest tarball URL based on the major version input
  tarball_url=$(curl -s https://www.kernel.org | grep -Eo "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${major_version}\.[0-9]*.tar.xz" | uniq)
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
done

