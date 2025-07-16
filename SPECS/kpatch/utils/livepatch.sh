#!/bin/bash
print_help() {
    echo "Usage: $(basename "$0") [options]"
    echo
    echo "This script automates the process of building a livepatch kernel module targeting a specified Photon OS kernel version and flavor."

cat << EOF

Options:
  -p <patches>           Specify a space-separated list of patch files. At least one patch must be listed.
  -k <kernel_version>    Specify the kernel version to patch. Defaults to building against the native kernel version if not specified.
  -n <module_name>       Specify the output .ko module name. Defaults to an auto-generated name if not specified.
  -o <output_dir>        Specify the output directory. Defaults to $0/output/ if not specified.
  -R                     Disable setting the replace flag in the livepatch module. The replace flag is enabled by default. (Passed to kpatch-build.)
  --export-debuginfo     Save debug files such as the patched vmlinux, modified object files, and related artifacts.
  -d <file>              Use the contents of file as the livepatch module's description, else use comment from patch file as description.
  -s <source_rpm>        Specify the path to a local Linux source RPM for building the livepatch. If not specified, required files will be downloaded automatically.
  -v <debuginfo_rpm>     Specify the path to a local Linux debuginfo RPM for symbol resolution. If not specified, required files will be downloaded automatically.
  --rpm                  Package the kernel module as an RPM.
  --rpm-version <ver>    Specify the version number for the RPM package.
  --rpm-release <rel>    Specify the release number for the RPM package.
  --rpm-desc <file>      Specify a description file for the RPM. Defaults to using the module description if not specified.
  --verbose              Print detailed logs of curl, rpmbuild and other operations.
  --sign                 Sign release artifacts using the signc script provided in the build infrastructure. Applicable only for GoBuild targets.
  --signer-id <id>       User ID assigned by GoBuild infrastructure for builds.
  --signer-name <name>   User name assigned by GoBuild infrastructure for builds.
  -h, --help             Display this help message and exit.

Examples:
  1. Build a basic livepatch module:
     $0 -k 5.10.12-1.ph3 -p fix_bug-01.patch fix_bug-02.patch

  2. Build and package the livepatch module as an RPM:
     $0 -k 5.10.12-1.ph3 -p fix_bug.patch --rpm --rpm-version 1.0 --rpm-release 1

  3. Build using local source and debuginfo RPMs:
     $0 -k 5.10.12-1.ph3 -p fix_bug.patch -s /path/to/kernel.src.rpm -v /path/to/debuginfo.rpm

  If GEN_LIVEPATCH_DEBUG is set to 1, the temporary directory will be preserved after the script completes. This is useful for debugging.
EOF
  exit $1
}

error() {
    if [[ -z "$1" ]]; then
        echo "Error! Exiting." 1>&2
    else
        echo "Error: $1" 1>&2
    fi
    exit 1
}

is_in_array() {
    local opt=$1
    shift
    while (( $# )); do
        [[ "$opt" == "$1" ]] && return 0
        shift
    done
    return 1
}

check_permission() {
  if ! docker info > /dev/null 2>&1; then
    error "Docker daemon is not running or not accessible. Try starting Docker using: sudo systemctl start docker"
  fi
}
