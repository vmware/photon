#!/bin/bash

# This script is designed to create a livepatch module for the specified Photon OS kernel version.
# Args:
#       -k: Specifies the kernel version. If not set, builds native livepatch
#       -p: Patch file list. Need at least one patch file listed here
#       -n: Output file name. Will be default if not specified.
#       -o: Output folder for livepatch modules.
#       -R: Don't set replace flag for the livepatch module. Default is to set the flag.
#       --export-debuginfo: Save debug files such as patched vmlinux, changed objs, etc.
#       -h/--help: Prints help message
#       -d: Use file contents as description field for livepatch module.
#       --rpm: Package the kernel module as an rpm
#       --rpm-version: Specify the version number of the rpm
#       --rpm-release: Specify the release number of the rpm
#       --rpm-desc: Specify the description file for the rpm. If not set, it will be the same as the module.
#
# ex)
#   With all options enabled, and multiple patches:
#       gen_livepatch -k 4.19.247-2.ph3 -o my_dir -n my_livepatch.ko -p my_patch1.patch my_patch2.patch -D description.txt -R --export-debuginfo
# ex)
#    All default settings. Must supply at least one patch file though. Builds a livepatch for the current kernel version
#       gen_livepatch -p my_patch.patch
#
# If GEN_LIVEPATCH_DEBUG is set to 1, the tmp directory will not be deleted at the end of the script. Useful for debugging purposes.

set -o pipefail

GCC=/usr/bin/gcc
BUILD_DIR="/var/opt/gen_livepatch"
DEFAULT_OUTPUT_FOLDER="$BUILD_DIR/livepatches"
TEMP_DIR="$BUILD_DIR/tmp"
SRC_DIR="$TEMP_DIR/rpmbuild/BUILD"
VERSION_RELEASE_FLAVOR=""
OUTPUT_FOLDER=""
LIVEPATCH_NAME=""
LIVEPATCH_EXT="_klp"
DEBUG_PKGNAME=""
SRC_PKGNAME=""
SPEC_FILENAME=""
VMLINUX_PATH=""
STARTING_DIR="$PWD"
PH_TAG=""
KERNEL_RELEASE=""
KERNEL_FLAVOR=""
KERNEL_VERSION=""
KERNEL_VERSION_RELEASE_TAG=""
KERNEL_RELEASE_TAG=""
IS_RT=0
NON_REPLACE_FLAG=""
EXPORT_DEBUGINFO=0
DEBUGINFO_DIR="$BUILD_DIR/debuginfo"
KPATCH_BUILDDIR="$HOME/.kpatch"
DESC_FILE=""
RPM_DESCFILE=""
PACKAGE_AS_RPM=0
RPM_VERSION=""
RPM_RELEASE=""
BUILD_RPM_SPECFILE="/etc/gen_livepatch/build-rpm.spec"
DEBUGINFO_LOCAL_PATH=""
RPM_MACRO_FILE=""
HAS_DIST_TAG=1
patches=()

# args
#   1. string to match
#   2. array values
match_string_in_array() {
    local string_to_match=$1
    shift
    while (( $# )); do
        if [[ "$string_to_match" == "$1" ]]; then
            return 0
        fi
        shift
    done

    return 1
}

# parse the command line arguments and fill in variables
parse_args() {
    # just print help message if no arguments
    if [ $# -eq 0 ]; then
        print_help 0
    elif [[ $1 != -* ]]; then
        echo "A flag must be set before any other parameters"
        print_help 1
    fi

    local flag=""
    flags=( "-s" "-p" "-v" "-o" "-h" "--help" "-k" "-n" "-R" "--export-debuginfo" "-d" "--rpm" "--rpm-version" "--rpm-release" "--rpm-desc" )
    while (( "$#" )); do
        if [[ $1 = -* ]]; then
            flag=$1

            # check to make sure number of args are correct
            if ! match_string_in_array $flag ${flags[@]} ; then
                error "Unknown option $flag"
            elif [[ $1 == -h || $1 == --help ]]; then
                print_help 0
            elif [[ $1 == -R ]]; then
                NON_REPLACE_FLAG="-R"
            elif [[ $1 == --export-debuginfo ]]; then
                EXPORT_DEBUGINFO=1
            elif [[ $1 == --rpm ]]; then
                PACKAGE_AS_RPM=1
            elif [[ $2 == -* || -z $2 ]]; then
                error "$1 needs at least one argument"
            elif  [[ $3 != -* && $flag != -p && -n $3 ]]; then
                error "$1 only takes one argument"
            fi
        else
            case "$flag" in
                -p)
                    patches+=("$1")
                    ;;
                -k)
                    VERSION_RELEASE_FLAVOR=$1
                    ;;
                -o)
                    OUTPUT_FOLDER=$1
                    ;;
                -n)
                    LIVEPATCH_NAME=$1
                    ;;
                -d)
                    DESC_FILE=$1
                    [ -f "$DESC_FILE" ] || error "Module description file does not exist"
                    ;;
                -s)
                    SRC_RPM_LOCAL_PATH=$1
                    [ -f "$SRC_RPM_LOCAL_PATH" ] || error "Unable to locate local src rpm at $SRC_RPM_LOCAL_PATH"
                    ;;
                -v)
                    DEBUGINFO_LOCAL_PATH=$1
                    [ -f "$DEBUGINFO_LOCAL_PATH" ] || error "Unable to locate local debuginfo rpm at $DEBUGINFO_LOCAL_PATH"
                    ;;
                --rpm-version)
                    RPM_VERSION=$1
                    ;;
                --rpm-release)
                    RPM_RELEASE=$1
                    ;;
                --rpm-desc)
                    RPM_DESCFILE=$1
                    [ -f "$RPM_DESCFILE" ] || error "RPM description file does not exist"
                    ;;
                esac
        fi
        # shift to the next argument
        shift
    done

    if [ -z "$patches" ]; then
        error "Please input at least one patch file"
    fi

    if [ -z "$VERSION_RELEASE_FLAVOR" ]; then
        echo "No kernel version specified, building native patch"
        VERSION_RELEASE_FLAVOR=$(uname -r)
    fi

    if [ -z "$LIVEPATCH_NAME" ]; then
        echo "No output name specified, using default"
        # just use the first 20 characters of the patch file name
        local first_patch_name=$(cut -d '.' -f 1 <<< "$(basename "${patches[0]}")")
        local cur_datetime=$(date +%d%b%Y-%H_%M_%S)
        LIVEPATCH_NAME=${first_patch_name}-${cur_datetime}${LIVEPATCH_EXT}
    fi

    if [ -z "$OUTPUT_FOLDER" ]; then
        echo "Output folder not specified, using default."
        echo "Outputting livepatches to: $DEFAULT_OUTPUT_FOLDER"
        OUTPUT_FOLDER="$DEFAULT_OUTPUT_FOLDER"
    fi

    if [[ -z "$RPM_VERSION" && "$PACKAGE_AS_RPM" == 1 ]]; then
        echo "RPM version number not specified, setting to 1"
        RPM_VERSION=1
    fi

    if [[ -z "$RPM_RELEASE" && "$PACKAGE_AS_RPM" == 1 ]]; then
        echo "RPM release not specified, setting to 1"
        RPM_RELEASE=1
    fi

    # if building an rpm, and rpm description is not specified, use the kernel module desc file if it is set
    if [[ ! -z "$DESC_FILE" && "$PACKAGE_AS_RPM" == 1 && -z "$RPM_DESCFILE" ]]; then
        echo "Separate RPM description not specified, using module description"
        RPM_DESCFILE=$DESC_FILE
    fi

    # make sure output folder exists
    mkdir -p "$OUTPUT_FOLDER"

    # remove .ko if it's added, otherwise resulting kernel module will have wrong name
    if [[ "${LIVEPATCH_NAME##*.}" == "ko" ]]; then
        LIVEPATCH_NAME="${LIVEPATCH_NAME%.*}"
    fi

    is_rt "$VERSION_RELEASE_FLAVOR"
    get_kernel_flavor "$VERSION_RELEASE_FLAVOR"
    get_kernel_version "$VERSION_RELEASE_FLAVOR"
    get_kernel_release "$VERSION_RELEASE_FLAVOR"
    get_photon_tag "$VERSION_RELEASE_FLAVOR"

    KERNEL_VERSION_RELEASE_TAG=${KERNEL_VERSION}-${KERNEL_RELEASE}.${PH_TAG}
    KERNEL_RELEASE_TAG=${KERNEL_RELEASE}.${PH_TAG}

    # Add dist tag to rpm macros file to better handle rpmbuild of linux src rpm
    if [ "$(rpm -E %dist)" == "%dist" ]; then
        echo "%dist .$PH_TAG" >> "$HOME"/.rpmmacros || error "Failed to define %dist tag in $HOME/.rpmmacros"

        # record RPM macro file as whatever file we edited here, so we can reverse
        # this change at the end of the build
        RPM_MACRO_FILE="$HOME/.rpmmacros"
        HAS_DIST_TAG=0
    fi
}

# takes in uname -r formatted string
# ex) 4.19.247-2.ph3-aws
get_kernel_flavor() {
    # check for rt kernel extension
    if [[ $IS_RT != 1 ]]; then
        KERNEL_FLAVOR=$(cut -d '-' -f 3 <<< "$1")
        if [ -z "$KERNEL_FLAVOR" ]; then
            KERNEL_FLAVOR="generic"
        fi
    else
        KERNEL_FLAVOR=rt
    fi
}

is_rt() {
    local rt_ext="$(cut -d '-' -f 4 <<< "$1")"
    if [[ -n $rt_ext ]]; then
        IS_RT=1
    fi
}

# takes in uname -r formatted string
# returns the release number
get_kernel_release() {
    local field_num=2
    if [[ $IS_RT == 1 ]]; then
        # rt kernel
        field_num=3
    fi

    local release_tag=$(cut -d '-' -f $field_num <<< "$1")
    local release=$(cut -d '.' -f 1 <<< "$release_tag")
    KERNEL_RELEASE=$release
}

# takes in uname -r formatted string
# gets kernel version only
# ex) 5.10.118
get_kernel_version() {
    KERNEL_VERSION=$(cut -d '-' -f 1 <<< "$1")
}

# extracts .phX tag from
# uname -r formatted string
get_photon_tag() {
    local field_num=2
    if [[ $IS_RT == 1 ]]; then
        # rt kernel
        field_num=3
    fi

    local release_tag=$(cut -d '-' -f $field_num <<< "$1")
    local kernel_tag=$(cut -d '.' -f 2 <<< "$release_tag")
    PH_TAG=$kernel_tag
}

print_config() {
    echo -e "\nBuilding livepatch"
    echo -e "Linux Version: $KERNEL_VERSION_RELEASE_TAG"
    echo -e "Photon OS Version: $PHOTON_VERSION"
    echo -e "Photon OS Flavor: $KERNEL_FLAVOR"
    echo -e "Patch files: "
    for patch in "${patches[@]}"; do
        echo -e "\t $(basename "$patch")"
    done
}

# Copied from kpatch-build. Used to find gcc version that was used to compile an executable
gcc_version_from_file() {
    readelf -p .comment "$1" | grep -m 1 -o 'GCC:.*' || error "Error with readelf"
}

# Copied from kpatch-build. Used to check if GCC versions match
gcc_version_check() {
    local target="$1"
    local c="$BUILD_DIR/gcc_version_check.c"
    local o="$BUILD_DIR/gcc_version_check.o"
    local out gccver kgccver

    # gcc --version varies between distributions therefore extract version
    # by compiling a test file and compare it to vmlinux's version.
    echo 'int main(void) {return 0;}' > "$c"
    out="$("$GCC" -c -pg -ffunction-sections -o "$o" "$c" 2>&1)"
    if [[ $? != 0 ]]; then
        error "GCC compilation error"
    fi

    if [[ -n "$out" ]]; then
        echo "gcc >= 4.8 required for -pg -ffunction-settings"
        echo "gcc output: $out"
        error
    fi

    gccver="$(gcc_version_from_file "$o")"
    kgccver="$(gcc_version_from_file "$target")"

    rm -f "$c" "$o"

    # ensure gcc version matches that used to build the kernel
    if [[ "$gccver" != "$kgccver" ]]; then
        echo "gcc/kernel version mismatch"
        echo "gcc version:    $gccver"
        echo "kernel version: $kgccver"
        echo "kpatch may have problems when building with the wrong gcc, exiting to be safe..."
        error
    fi
}

# prints error message and then exits
error() {
    if [[ -z "$1" ]]; then
        echo "Error! Exiting." 1>&2
    else
        echo "ERROR: $1" 1>&2
    fi

    #clean up before exiting
    if [[ $GEN_LIVEPATCH_DEBUG != 1 ]]; then
        rm -rf $TEMP_DIR
    fi
    exit 1
}


print_help() {
    echo -e "This script is designed to create a livepatch module for the specified Photon OS kernel version and flavor."
    echo -e "Arguments:"
    echo -e "\t -k: Specifies the kernel version. If not set, builds native livepatch"
    echo -e "\t -p: Patch file list. Need at least one patch file listed here"
    echo -e "\t -n: Output file name. Will be default if not specified."
    echo -e "\t -o: Output directory. Will be default if not specified."
    echo -e "\t -R: Don't set the replace flag in the livepatch module. Replace flag is set by default."
    echo -e "\t --export-debuginfo: Save debug files such as patched vmlinux, changed objs, etc."
    echo -e "\t -h/--help: Print help message"
    echo -e "\t -d: Use file contents as description field for livepatch module."
    echo -e "\t -s: Specify the location of a local copy of the Linux src rpm to use"
    echo -e "\t -v: Specify the location of a local copy of the Linux debuginfo rpm to use"
    echo -e "\t --rpm: Package the kernel module as an rpm"
    echo -e "\t --rpm-version: Specify the version number of the rpm"
    echo -e "\t --rpm-release: Specify the release number of the rpm"
    echo -e "\t --rpm-desc: Specify the description file for the rpm. If not set, it will be the same as the module."
    exit "$1"
}

install_kernel_dependencies() {
    local to_be_installed_pkgs=($(rpm -qpR "$1" | grep -vw rpmlib))
    echo -e "The following packages must be installed:\n${to_be_installed_pkgs[*]}\n"
    tdnf install -qy "${to_be_installed_pkgs[@]}" || error "Error installing required packages"
}

parse_source_rpm() {
    echo -e "\nDownloading and/or processing source rpm"
    local src_rpm_url="https://packages.vmware.com/photon/${PHOTON_VERSION}/photon_srpms_${PHOTON_VERSION}_x86_64/$SRC_PKGNAME"

    # allow downloading/copying of source rpm from either local or custom urls. Just need these variables to be exported before
    # running to enable these options.
    if [ -n "${SRC_RPM_LOCAL_PATH}" ]; then
        cp "$SRC_RPM_LOCAL_PATH" "$SRC_PKGNAME" || error "Couldn't find local src rpm"
    elif [ -n "${SRC_RPM_REMOTE_URL}" ]; then
        curl "$SRC_RPM_REMOTE_URL" --output "$SRC_PKGNAME"  &> /dev/null || error "Couldn't download remote src rpm"
    else
        curl "$src_rpm_url" --output "$SRC_PKGNAME"  &> /dev/null || error "Couldn't download photon kernel source rpm"
    fi

    # set up temporary rpm build environment
    local rpmdir="%_topdir %(echo $PWD)/rpmbuild"
    mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} || error

    rpm -i "$SRC_PKGNAME" --define "$rpmdir" || error "Failed to extract spec file"
    local config_filename=$(awk '/^Source1:/{print $NF}' rpmbuild/SPECS/linux*.spec)
    if [[ "$config_filename" = "config_%{_arch}" ]]; then
        config_filename="config_x86_64"
    fi

    install_kernel_dependencies "$SRC_PKGNAME"

    rpmbuild -bp "rpmbuild/SPECS/$SPEC_FILENAME" --define "$rpmdir" &> /dev/null || error "Failed to extract kernel source and create linux source directory"

    echo "Copying source files to correct locations, if they exist"
    ls rpmbuild/BUILD/fips*canister* &> /dev/null && cp -rT rpmbuild/BUILD/fips*canister* "rpmbuild/BUILD/linux-$KERNEL_VERSION/crypto"
    cp rpmbuild/SOURCES/"$config_filename" rpmbuild/BUILD/linux-"$LINUX_VERSION"/.config || error "Failed to locate kernel config file"
    [[ -f rpmbuild/SOURCES/fips_canister-kallsyms ]] && cp rpmbuild/SOURCES/fips_canister-kallsyms "rpmbuild/BUILD/linux-$LINUX_VERSION/crypto"

    if [[ "$KERNEL_FLAVOR" == "esx" ]] || [[ "$KERNEL_FLAVOR" == "rt" ]]; then
        # change m to y for fips canister
        cp "rpmbuild/SOURCES/modify_kernel_configs.inc" "rpmbuild/BUILD/linux-$LINUX_VERSION"
        pushd "rpmbuild/BUILD/linux-$LINUX_VERSION"  &> /dev/null || error
        source "modify_kernel_configs.inc"
        popd  &> /dev/null || error
    fi

    # make sure vermagic gets the right tag, otherwise kpatch load may fail
    # basically just make sure vermagic in modinfo is the same as uname -r
    if [[ $KERNEL_FLAVOR == "generic" ]]; then
        sed -i s/^CONFIG_LOCALVERSION=\".*\"/CONFIG_LOCALVERSION=\"-$KERNEL_RELEASE_TAG\"/g rpmbuild/BUILD/linux-"$LINUX_VERSION"/.config
    else
        sed -i s/^CONFIG_LOCALVERSION=\".*\"/CONFIG_LOCALVERSION=\"-$KERNEL_RELEASE_TAG-$KERNEL_FLAVOR\"/g rpmbuild/BUILD/linux-"$LINUX_VERSION"/.config
    fi
}

parse_debuginfo_rpm() {
    echo -e "\nDownloading debug package and extracting vmlinux"

    if [[ -n "$DEBUGINFO_LOCAL_PATH" ]]; then
        cp "$DEBUGINFO_LOCAL_PATH" "$DEBUG_PKGNAME"
    else
        curl "https://packages.vmware.com/photon/$PHOTON_VERSION/photon_debuginfo_${PHOTON_VERSION}_x86_64/x86_64/$DEBUG_PKGNAME" --output "$DEBUG_PKGNAME"  &> /dev/null || error
    fi

    local absolute_path=$(rpm -qlp "$DEBUG_PKGNAME" | grep "vmlinux-$LINUX_VERSION")

    # remove the first slash from the path
    VMLINUX_PATH=${absolute_path:1}

    # extract vmlinux
    rpm2cpio "$DEBUG_PKGNAME" | cpio -ivd "./$VMLINUX_PATH"  &> /dev/null || error "Couldn't extract vmlinux from $DEBUG_PKGNAME"
}

# sets all the variables for file names
# vmlinux path is set when we parse the debuginfo package
set_filenames_and_paths() {
    #determine which photon version this is
    PHOTON_VERSION="${PH_TAG//[^0-9]/}".0

    #determine which linux version this is
    LINUX_VERSION=$(cut -d '-' -f 1 <<< $KERNEL_VERSION_RELEASE_TAG)

    #set file paths based on kernel flavor
    if [[ "$KERNEL_FLAVOR" == "generic" ]]; then
        DEBUG_PKGNAME="linux-debuginfo-$KERNEL_VERSION_RELEASE_TAG.x86_64.rpm"
        SRC_PKGNAME="linux-$KERNEL_VERSION_RELEASE_TAG.src.rpm"
        SPEC_FILENAME="linux.spec"
    else
        DEBUG_PKGNAME="linux-$KERNEL_FLAVOR-debuginfo-$KERNEL_VERSION_RELEASE_TAG.x86_64.rpm"
        SRC_PKGNAME="linux-$KERNEL_FLAVOR-$KERNEL_VERSION_RELEASE_TAG.src.rpm"
        SPEC_FILENAME="linux-$KERNEL_FLAVOR.spec"
    fi
}

#executes the kpatch-build command to build the livepatch
kpatch_build() {
    #only need -R flag for 3.0, since 3.0 doesn't support klp_replace
    #otherwise leave it as set by the user
    if [[ $PHOTON_VERSION == "3.0" ]]; then
        NON_REPLACE_FLAG="-R"
    fi

    local skip_cleanup=""
    if [[ $EXPORT_DEBUGINFO == 1 ]]; then
        skip_cleanup="--skip-cleanup"
    fi

    local description_file=""
    if [ -f "$DESC_FILE" ]; then
        description_file="-D $DESC_FILE"
    fi

    kpatch-build -v "$TEMP_DIR/$VMLINUX_PATH" \
            -s "$TEMP_DIR/rpmbuild/BUILD/linux-$LINUX_VERSION" \
            -c "$TEMP_DIR/rpmbuild/BUILD/linux-$LINUX_VERSION/.config" \
            -j "$(nproc)" \
            -n "$LIVEPATCH_NAME" \
            -o "$OUTPUT_FOLDER" \
            "${patches[@]}" \
            $NON_REPLACE_FLAG \
            $skip_cleanup \
            $description_file \
            || error "Building livepatch module failed."
    echo "Livepatch module successfully built"

    # save all of the debug info like vmlinux, changed objects, etc if asked to
    # vmlinux is the patched vmlinux, not original
    if [[ $EXPORT_DEBUGINFO == 1 ]]; then
        echo "Saving kpatch-build debug files to $DEBUGINFO_DIR"

        # clean out any old files
        if [[ -n "$DEBUFINFO_DIR" ]]; then
            rm -r "${DEBUGINFO_DIR:?}"/*  &> /dev/null
        fi

        mkdir -p $DEBUGINFO_DIR/patched-debuginfo
        cp $SRC_DIR/linux-"$KERNEL_VERSION"/vmlinux* \
           $SRC_DIR/linux-"$KERNEL_VERSION"/modules* \
           $SRC_DIR/linux-"$KERNEL_VERSION"/Module.symvers \
           $DEBUGINFO_DIR/patched-debuginfo
        cp -r "$KPATCH_BUILDDIR"/tmp "$DEBUGINFO_DIR"/kpatch-tmp
    fi
}


# function to package the required module inside of an rpm
package_module_in_rpm() {
    echo -e "\nPreparing to build rpm"

    local linux_version
    [[ "$KERNEL_FLAVOR" == "generic" ]] && linux_version="$KERNEL_VERSION_RELEASE_TAG" || linux_version="${KERNEL_VERSION_RELEASE_TAG}-${KERNEL_FLAVOR}"

    pushd "$TEMP_DIR" > /dev/null 2>&1 || error
    # set up temporary rpm build environment
    local rpmdir="%_topdir %(echo $PWD)/rpmbuild"
    mkdir -p rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS} || error
    popd > /dev/null 2>&1 || error

    cd "$STARTING_DIR" > /dev/null 2>&1 || error
    mv "$OUTPUT_FOLDER"/"$LIVEPATCH_NAME".ko "$TEMP_DIR"/rpmbuild/SOURCES || error

    # fill in needed info in spec file skeleton
    local spec_file="$TEMP_DIR/rpmbuild/SPECS/build-rpm.spec"
    cp "$BUILD_RPM_SPECFILE" "$spec_file" || error
    sed -i "s/@@VERSION@@/$RPM_VERSION/g" "$spec_file" || error "Filling in RPM vesion for spec file skeleton failed"
    sed -i "s/@@RELEASE@@/$RPM_RELEASE/g" "$spec_file" || error "Filling in RPM release for  spec file skeleton failed"
    sed -i "s/@@LIVEPATCH_NAME@@/$LIVEPATCH_NAME/g" "$spec_file" || error "Filling in livepatch name for spec file skeleton failed"
    sed -i "s/@@LINUX_VERSION@@/$linux_version/g" "$spec_file" || error "Filling in linux version for spec file skeleton failed"

    if [ -f "$RPM_DESCFILE" ]; then
        sed -i "s/@@DESCRIPTION@@/$(cat "$RPM_DESCFILE")/g" "$spec_file" || error "Filling in description for spec file skeleton failed"
    else
        sed -i "s/@@DESCRIPTION@@/Livepatch module for Linux $linux_version\n/g" "$spec_file" || error "Filling in description for spec file skeleton failed"
    fi

    echo "Building rpm"
    rpmbuild -bb $spec_file --define "$rpmdir" > /dev/null 2>&1 || error "Packaging kernel module as rpm failed"

    # should only build for x86_64 arch but put a * there just in case
    cp "$TEMP_DIR"/rpmbuild/RPMS/*/"$LIVEPATCH_NAME"*.rpm "$OUTPUT_FOLDER" || error "Current dir: $STARTING_DIR. Failed to save RPM to $OUTPUT_FOLDER"

    echo "SUCCESS: Building rpm finished"
}

cleanup() {
    if [[ $GEN_LIVEPATCH_DEBUG != 1 ]]; then
        rm -rf $TEMP_DIR || error "Failed to delete temp dir: $TEMP_DIR"
    fi
    [[ "$HAS_DIST_TAG" -eq 0 ]] && sed -i "/%dist .$PH_TAG/d" "$RPM_MACRO_FILE"
}

#cleanup on exit
trap cleanup EXIT SIGINT SIGTERM

#make sure our working directory is clean before we start
rm -rf $TEMP_DIR

#parse command line arguments
parse_args "$@"

#set variables for all filenames/paths
set_filenames_and_paths

print_config

mkdir -p $TEMP_DIR
cd $TEMP_DIR || error

#download, prep, kernel source
parse_source_rpm

#download and extract vmlinux
parse_debuginfo_rpm

#execute kpatch-build with all of the required args
gcc_version_check "$VMLINUX_PATH"

echo -e "\nAll sources ready, building livepatch module..."
# cd back to starting directory so that patch file paths are correct
cd "$STARTING_DIR" || error
kpatch_build

if [[ $PACKAGE_AS_RPM == 1 ]]; then
    package_module_in_rpm
fi
