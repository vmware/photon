#!/bin/bash

# Wrapper script for gen_livepatch.sh. Runs gen_livepatch.sh inside
# of a docker container. Makes it much easier to install dependencies,
# control build environment, etc.
#
# Args:
#   -k: Specifies the kernel version. If not set, builds native livepatch
#   -p: Patch file list. Need at least one patch file listed here
#   -n: Output file name. Will be default if not specified.
#   -o: Output directory for livepatch modules
#   -R: Don't set replace flag in livepatch module. Replace flag is set by default.
#   -d: Use file contents as description field for livepatch module.
#   --export-debuginfo: Save debug files such as patched vmlinux, changed objs, etc.
#   -h/--help: Prints help message
#   --rpm: Package the kernel module as an rpm
#   --rpm-version: Specify the version number of the rpm
#   --rpm-release: Specify the release number of the rpm
#   --rpm-desc: Specify the description file for the rpm. If not set, it will be the same as the module.
#
#
# ex)
#   With all options enabled, and multiple patches:
#       auto_livepatch -k 4.19.247-2.ph3 -o my_dir -n my_livepatch.ko -p my_patch1.patch my_patch2.patch -d description.txt
# ex)
#    All default settings. Must supply at least one patch file though. Builds a livepatch for the current kernel version
#       auto_livepatch -p my_patch.patch

set -o pipefail

# keeps track of what version of kpatch-utils this is
# very important to know when to rebuild the docker images
VERSION_TAG=4

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root user"
    exit 1
fi

# check to make sure docker is installed and running
if [[ $(systemctl is-active docker) != active ]]; then
    echo "Looks like docker is either not installed or not running. Please install or start docker"
    echo "To install: tdnf install docker"
    echo "To start: systemctl start docker"
    exit 1
fi

AUTO_LIVEPATCH_DIR=/var/opt/auto_livepatch
DOCKER=/usr/bin/docker
DEFAULT_OUTPUT_DIR=$AUTO_LIVEPATCH_DIR/livepatches
DEBUGINFO_DIR=$AUTO_LIVEPATCH_DIR/debuginfo
OUTPUT_DIR=$DEFAULT_OUTPUT_DIR
ARGS=""
PH_TAG=""
DOCKER_BUILDDIR=/var/opt/gen_livepatch
DOCKER_LIVEPATCH_DIR=$DOCKER_BUILDDIR/livepatches
DOCKER_IMAGE_NAME=""
DOCKER_DEBUGINFO_DIR=/var/opt/gen_livepatch/debuginfo
DOCKER_CONTAINER_NAME=""
DOCKERFILE_NAME=""
DOCKERFILE_DIR=/etc/auto_livepatch/dockerfiles
PATCH_DIR=$AUTO_LIVEPATCH_DIR/patches
DOCKER_KPATCH_BUILDLOG=/root/.kpatch/build.log
FAILED=0
EXPORT_DEBUGINFO=0
DESC_GIVEN=0
RPM_DESC_GIVEN=0
SRC_RPM_LOCAL_PATH=""
DEBUGINFO_LOCAL_PATH=""

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

gen_dockerfile() {
    local dockerfile=$DOCKERFILE_DIR/$DOCKERFILE_NAME

    [[ -d $DOCKERFILE_DIR ]] || mkdir -p $DOCKERFILE_DIR

    # don't need to rebuild if already present
    [[ -f "$dockerfile" ]] && return 0

    local pkgs_req=( "build-essential" \
                     "elfutils-libelf-devel" \
                     "tar" \
                     "findutils" \
                     "audit-devel" \
                     "binutils-devel" \
                     "elfutils-devel" \
                     "gdb" \
                     "glib-devel" \
                     "kmod-devel" \
                     "libcap-devel" \
                     "libunwind-devel" \
                     "openssl-devel" \
                     "pciutils-devel" \
                     "procps-ng-devel" \
                     "python3-devel" \
                     "slang-devel" \
                     "xz-devel" \
                     "rpm-build" \
                     "bc" \
                     "Linux-PAM-devel" \
                     "kbd" \
                     "libdnet-devel" \
                     "libmspack-devel" \
                     "xerces-c-devel" \
                     "coreutils" \
                     "util-linux" \
                     "kpatch" \
                     "kpatch-build" \
                     "kpatch-utils" )

    echo "FROM photon:${PH_TAG//[^0-9]/}.0" > $dockerfile
    echo "RUN tdnf install -y \\" >> $dockerfile
    for pkg in ${pkgs_req[@]}; do
        if [[ "$pkg" == "${pkgs_req[-1]}" ]]; then
          echo "$pkg" >> $dockerfile
        else
          echo "$pkg \\" >> $dockerfile
        fi
    done
}

# just get what we need for this script from the arguments.
# do some error checking here so that it will error out before creating
# docker container, which could take some time if the image is not
# already created.
parse_args() {
    # just print help message if no arguments
    if [ $# -eq 0 ]; then
        source gen_livepatch.sh
    elif [[ $1 != -* ]]; then
        echo "Flag must be set before any other parameters"
        exit 1
    fi

    mkdir -p $PATCH_DIR
    local flag=""
    local patch_given=0
    local flags=( "-s" "-v" "-p" "-o" "-h" "--help" "-k" "-n" "-R" "--export-debuginfo" "-d" "--rpm" "--rpm-version" "--rpm-release" "--rpm-desc" )
    local no_arg_flags=( "-R" "--export-debuginfo" "-h" "--help" "--rpm" )
    while (( "$#" )); do
        arg=$1
        if [[ $1 == -* ]]; then
            flag=$1

            if ! match_string_in_array $flag ${flags[@]}; then
                error "Unknown option $flag"
            elif [[ $1 == -h || $1 == --help ]]; then
                source gen_livepatch.sh
                exit 0
            elif [[ $1 == --export-debuginfo ]]; then
                EXPORT_DEBUGINFO=1
            elif ! match_string_in_array $flag ${no_arg_flags[@]} && [[ ($2 == -* || -z $2) ]]; then
                error "$1 needs at least one argument"
            elif  [[ $3 != -* && $flag != -p && -n $3 ]] && ! match_string_in_array $flag ${no_arg_flags[@]} ; then
                error "$1 only takes one argument"
            fi
        else
            case "$flag" in
                -p)
                    patch_given=1
                    cp "$1" $PATCH_DIR &> /dev/null || error "Couldn't find patch file $1"
                    arg="$DOCKER_BUILDDIR/patches/$(basename "$arg")"
                    ;;
                -k)
                    VERSION_RELEASE_FLAVOR=$1
                    ;;
                -o)
                    OUTPUT_DIR=$1
                    ;;
                -d)
                    DESC_GIVEN=1
                    cp "$1" "$AUTO_LIVEPATCH_DIR/description.txt" &> /dev/null || error "Description file $1 not found"
                    ;;
                --rpm-desc)
                    RPM_DESC_GIVEN=1
                    cp "$1" "$AUTO_LIVEPATCH_DIR/rpm-description.txt" &> /dev/null || error "RPM description file $1 not found"
                    ;;
                -s)
                    SRC_RPM_LOCAL_PATH=$1
                    ;;
                -v)
                    DEBUGINFO_LOCAL_PATH=$1
                    ;;
                esac
        fi

        # pass all arguments except for output directory into docker container
        if [[ $flag != "-o" ]] && [[ $flag != "-d" ]] && [[ $flag != "--rpm-desc" ]] && [[ $flag != "-s" ]] && [[ $flag != "-v" ]]; then
            if [ -z "$ARGS" ]; then
                ARGS="$arg"
            else
                ARGS="$ARGS $arg"
            fi
        fi

        # shift to the next argument
        shift
    done

    if [[ $patch_given -eq 0 ]]; then
        error "Please input at least one patch file"
    fi

    if [[ -n "$SRC_RPM_LOCAL_PATH" ]]; then
        ARGS="$ARGS -s $DOCKER_BUILDDIR/$(basename $SRC_RPM_LOCAL_PATH)"
    fi

    if [[ -n "$DEBUGINFO_LOCAL_PATH" ]]; then
        ARGS="$ARGS -v $DOCKER_BUILDDIR/$(basename $DEBUGINFO_LOCAL_PATH)"
    fi

    #make sure description file is easily accessible
    if [[ $DESC_GIVEN -eq 1 ]]; then
        ARGS="$ARGS -d $DOCKER_BUILDDIR/description.txt"
    fi

    if [[ $RPM_DESC_GIVEN -eq 1 ]]; then
        ARGS="$ARGS --rpm-desc $DOCKER_BUILDDIR/rpm-description.txt"
    fi

    # output livepatch(es) to the same folder in the docker container
    ARGS="$ARGS -o livepatches"

    if [ -z "$VERSION_RELEASE_FLAVOR" ]; then
        VERSION_RELEASE_FLAVOR=$(uname -r)
    fi

    [[ $VERSION_RELEASE_FLAVOR =~ \.ph[0-9]+ ]] && PH_TAG="${BASH_REMATCH:1}"

    if [ -z "$PH_TAG" ]; then
        echo "Wrong kernel version detected: $VERSION_RELEASE_FLAVOR"
        echo "Check for typos. Make sure it is in the same format as uname -r"
        exit 1
    fi

    DOCKER_IMAGE_NAME=livepatch-$PH_TAG-$VERSION_TAG
    DOCKER_CONTAINER_NAME=$PH_TAG-livepatch-container
    DOCKERFILE_NAME=Dockerfile.$PH_TAG
    gen_dockerfile
}

config_container() {
    echo "Configuring docker container"
    if [[ $OUTPUT_DIR == "$DEFAULT_OUTPUT_DIR" ]]; then
        echo "No output directory specified, outputting to $DEFAULT_OUTPUT_DIR"
        mkdir -p $DEFAULT_OUTPUT_DIR
    fi

    if [[ -z "$(docker images -q "$DOCKER_IMAGE_NAME" 2> /dev/null)" ]]; then
        # clean up old docker images from alternate versions
        $DOCKER rmi -f "$(docker images | grep livepatch-$PH_TAG | awk '{print $1}')" &> /dev/null

        echo "No existing docker image found, building..."
        $DOCKER build --network=host -f $DOCKERFILE_DIR/"$DOCKERFILE_NAME" -t "$DOCKER_IMAGE_NAME" . || error
    fi

    if [[ -n "$(docker ps -a -f "name=$DOCKER_CONTAINER_NAME" -q 2> /dev/null)" ]]; then
        # clean up old docker container if it is still lurking around
        $DOCKER rm -f "$DOCKER_CONTAINER_NAME" || error
    fi

    $DOCKER run --network=host -t -d --name "$DOCKER_CONTAINER_NAME" "$DOCKER_IMAGE_NAME" /bin/bash > /dev/null || error

    # copy all necessary files into docker container, put patches into patches folder
    $DOCKER exec -t "$DOCKER_CONTAINER_NAME" mkdir -p $DOCKER_LIVEPATCH_DIR || error
    $DOCKER cp $PATCH_DIR "$DOCKER_CONTAINER_NAME":$DOCKER_BUILDDIR/ || error
    if [[ $DESC_GIVEN -eq 1 ]]; then
        $DOCKER cp "$AUTO_LIVEPATCH_DIR/description.txt" "$DOCKER_CONTAINER_NAME":$DOCKER_BUILDDIR/ || error
    fi

    if [[ $RPM_DESC_GIVEN -eq 1 ]]; then
        $DOCKER cp "$AUTO_LIVEPATCH_DIR/rpm-description.txt" "$DOCKER_CONTAINER_NAME":$DOCKER_BUILDDIR/ || error
    fi

    if [[ -n "$SRC_RPM_LOCAL_PATH" ]]; then
        [[ -f "$SRC_RPM_LOCAL_PATH" ]] || error "Failed to find local src rpm at $SRC_RPM_LOCAL_PATH"
        $DOCKER cp "$SRC_RPM_LOCAL_PATH" "$DOCKER_CONTAINER_NAME":$DOCKER_BUILDDIR/ || error
    fi

    if [[ -n "$DEBUGINFO_LOCAL_PATH" ]]; then
        [[ -f "$DEBUGINFO_LOCAL_PATH" ]] || error "Failed to find local debuginfo rpm at $DEBUGINFO_LOCAL_PATH"
        $DOCKER cp "$DEBUGINFO_LOCAL_PATH" "$DOCKER_CONTAINER_NAME":$DOCKER_BUILDDIR/ || error
    fi

}

# prints error message and then exits
error() {
    if [[ -z "$1" ]]; then
        echo "Error! Exiting." 1>&2
    else
        echo "ERROR: $1" 1>&2
    fi

    exit 1
}

save_buildlog() {
    echo "Copying kpatch build log from docker container to $AUTO_LIVEPATCH_DIR"
    $DOCKER cp "$DOCKER_CONTAINER_NAME":"$DOCKER_KPATCH_BUILDLOG" $AUTO_LIVEPATCH_DIR &> /dev/null || error "Couldn't find kpatch build log"
}

cleanup() {
    # copy output (should just be livepatch module) from docker container
    mkdir -p "$OUTPUT_DIR"
    $DOCKER cp "$DOCKER_CONTAINER_NAME":$DOCKER_LIVEPATCH_DIR/. "$OUTPUT_DIR" || error

    # debug flag, save files if set, otherwise let them get deleted
    if [[ $EXPORT_DEBUGINFO == 1 ]]; then
        [ $FAILED ] || save_buildlog

        echo "Saving build debug files to $DEBUGINFO_DIR"
        mkdir -p $DEBUGINFO_DIR
        $DOCKER cp "$DOCKER_CONTAINER_NAME":$DOCKER_DEBUGINFO_DIR/. "$DEBUGINFO_DIR" || error "Couldn't find debug files"
    else
        rm -rf $PATCH_DIR
    fi

    if [[ $FAILED == 1 ]]; then
        save_buildlog
    fi

    # delete old description files
    rm -f "$AUTO_LIVEPATCH_DIR/description.txt"

    echo "Cleaning up docker container:"
    docker rm -f "$DOCKER_CONTAINER_NAME" || error "Failed to delete existing docker container: $DOCKER_CONTAINER_NAME"
}

# make sure things are cleaned up if interrupted, especially because this is a long process
trap cleanup SIGINT SIGTERM EXIT

parse_args "$@"

config_container

# run gen_livepatch.sh script
$DOCKER exec -w $DOCKER_BUILDDIR "$DOCKER_CONTAINER_NAME" gen_livepatch.sh $ARGS || FAILED=1
