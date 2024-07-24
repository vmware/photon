#!/bin/bash

# Builds Intel drivers i40e, iavf, ice, etc, for arbitrary kernel versions.
# Allows control on which patches are applied, and also builds new drivers
# if provided with a source tarball and patches.

set -o pipefail

# global vars
DNAME=
DVER=
KVER=
KFLAV=
KSHORTVER=
SRCTAR=
CUSTOM_TEMPLATE=
BUILD_SPEC=
PATCHES=()
DISABLE_PATCHES=0

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
SPEC_DIR="$SCRIPT_DIR/../../SPECS/kernels-drivers-intel"
BUILD_DIR="$SPEC_DIR/tmp-build-dir"
OUT_DIR="$SCRIPT_DIR/../../stage/SANDBOX_DRIVER_RPMS"
TMP_TXT="$(mktemp)"

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

error() {
    echo "$1"
    exit 1
}

print_help() {
    echo -e "Usage: ./build-intel-driver.sh <options>"
    echo "Arguments:"
    echo -e "\t --dname: Driver name (ex iavf, i40e, ice)"
    echo -e "\t --dver: Driver version (ex 4.9.5)"
    echo -e "\t --kver: Kernel version, as obtained by \'uname -r\' (ex 6.1.90-1.ph5-rt)"
    echo -e "\t --patch: Full path to patch file. If any patches are specified, only these patches will be used."
    echo -e "\t --disable-patches: Don't apply any patches during the build process"
    echo -e "\t --srctar: Path to source tarball"
    echo -e "\t --outdir: Output directory. Defaults to $OUT_DIR"
    exit 0
}

# parse the command line arguments
parse_args() {
    local flags=( "--dname" "--dver" "--kver" "--patch" "--disable-patches" "--srctar" "--outdir" "-h" "--help" )
    local flag=

    # just print help message if no arguments
    if [ $# -eq 0 ]; then
        print_help
    elif [[ $1 != -* ]]; then
        echo "Flag must be set before any other parameters"
        print_help
    fi

    while (( "$#" )); do
        if [[ $1 = -* ]]; then
            flag=$1

            # check to make sure number of args are correct
            if ! match_string_in_array "$flag" "${flags[@]}" ; then
                error "Unknown option $flag"
            elif [[ $1 == -h || $1 == --help ]]; then
                print_help
            elif [[ "$1" == "--disable-patches" ]]; then
                DISABLE_PATCHES=1
            elif [[ $2 == -* || -z $2 ]]; then
                error "$1 needs at least one argument"
            elif  [[ $3 != -* && -n $3 ]]; then
                error "$1 only takes one argument"
            fi
        else
            case "$flag" in
                --dname)
                    DNAME="$1"
                    ;;
                --dver)
                    DVER="$1"
                    ;;
                --kver)
                    KVER="$1"
                    ;;
                --disable-patches)
                    echo "disable patches!"
                    DISABLE_PATCHES=1
                    ;;
                --patch)
                    PATCHES+=("$(readlink -f "$1")")
                    ;;
                --srctar)
                    SRCTAR="$(readlink -f "$1")"
                    [[ ! -f "$SRCTAR" ]] && error "Couldn't find src tarball!"
                    ;;
                --outdir)
                    OUT_DIR="$1"
                    ;;
                esac
        fi
        # shift to the next argument
        shift
    done

    [[ -z "$KVER" ]] && error "--kver must be specified"
    [[ -z "$DNAME" ]] && error "--dname must be specified"
    [[ -z "$DVER" ]] && error "--dver must be specified"

    KFLAV="$(cut -d '-' -f 3 <<< "${KVER}")"
    [[ -n "$KFLAV" ]] && KFLAV="-${KFLAV}"
    KSHORTVER="$(cut -d '-' -f 1 <<< "${KVER}")"

    CUSTOM_TEMPLATE="${SPEC_DIR}/drivers-intel-$DNAME.spec.in"
    BUILD_SPEC="linux${KFLAV}-drivers-intel-$DNAME-$DVER-$KSHORTVER.spec"
}

# Find the patches from the latest current driver version
# Updates global patch variable
# arg 1. path to spec/spec template
find_latest_patches() {
    local latest_ver=
    local line=
    local regex_if_src_ver=
    local regex_patch="^Patch[0-9]+:"
    local inside_if=0

    latest_ver=$(grep -E "%if.*%{src_ver}" "$1" | grep -Eo "([0-9]+\.)+[0-9]+" | sort -V | tail -1)
    [[ "$?" -eq 0 ]] || error "Failed to find latest driver version from spec"

    regex_if_src_ver="^%if.*\%\{src_ver\}.*==.*\"$latest_ver\"?$"

    while IFS= read -r line; do
        if [[ "$line" =~ $regex_if_src_ver ]]; then
            inside_if=1
        elif [[ $inside_if -eq 1 ]] && [[ "$line" =~ $regex_patch ]]; then
            PATCHES+=("$(cut -d ':' -f 2 <<< "$line")")
        elif [[ "$line" =~ ^%endif ]]; then
            inside_if=0
        fi
    done < "$1"
}

# Generates our custom template
# args:
#       1: path to template spec
#       2: Output path
#       3. is new driver version?
#       4. use existing patches?
generate_custom_template() {
    local temp_path="$1"
    local output_path="$2"
    local is_new_dver="$3"
    local use_existing_patches="$4"

    local regex_if_src_ver="^%if.*\%\{src_ver\}.*==.*\"$DVER\"?$"
    local regex_sha512="^%define[[:space:]]+sha512[[:space:]]+$DNAME-\%\{src_ver\}[[:space:]]*=.*"
    local regex_patch="^Patch[0-9]+:.*"
    local regex_endif="^%endif"
    local regex_changelog="^%changelog"
    local regex_rel="^Release:"
    local inside_if=0
    local patch_num=0
    local line=
    local drel=

    cp "$temp_path" "$output_path"

    # no modification necessary
    if [[ "$is_new_dver" -eq 0 ]] && [[ "$use_existing_patches" -eq 1 ]]; then
        return
    # change the patches to custom, for existing driver version
    # want to leave everything else the same
    elif [[ "$is_new_dver" -eq 0 ]] && [[ "$use_existing_patches" -eq 0 ]]; then
        echo "" > "$output_path"

        while IFS= read -r line; do
            if [[ $inside_if -eq 1 ]] && [[ "$line" =~ $regex_sha512 ]]; then
                # pin all our new patches under the shasum line
                echo -e "$line" >> "$output_path"
                while [[ $patch_num -lt ${#PATCHES[@]} ]]; do
                    # insert new patches here
                    echo -e "Patch${patch_num}: $(basename "${PATCHES[$patch_num]}")\n" >> "$output_path"
                    patch_num=$((patch_num + 1))
                done

                # done with patches
                continue
            # skip all preexisting patches
            elif [[ $inside_if -eq 1 ]] && [[ "$line" =~ $regex_patch ]]; then
                    continue
            elif [[ "$line" =~ $regex_if_src_ver ]]; then
                inside_if=1
            elif [[ "$line" =~ $regex_endif ]]; then
                inside_if=0
            elif [[ "$line" =~ $regex_rel ]]; then
                drel=$(awk '{print $2}' <<< "$line" | cut -d '%' -f 1)
            fi

            echo -e "$line" >> "$output_path"
        done < "$temp_path"

        echo -e "* $(date +"%a %b %d %Y") Build Script <build-script@build.script> $DVER-$drel\n- Build driver $DNAME-$DVER with custom patches" > "$TMP_TXT"
        sed -i "/$regex_changelog/r $TMP_TXT" "$output_path"
    # new driver version
    elif [[ "$is_new_dver" -eq 1 ]]; then
        [[ -z $SRCTAR ]] && error "No source tarball given, cannot build new driver version"

        local new_section="\n%if \"%{src_ver}\" == \"$DVER\""
        new_section="$new_section\nRelease: 1%{?kernelsubrelease}%{?dist}"
        new_section="$new_section\n%define sha512 iavf-%{src_ver}=$(sha512sum "$SRCTAR" | awk '{print $1}' )\n"

        # add patches
        local i=0
        [[ "$use_existing_patches" -eq 1 ]] && find_latest_patches "$output_path"
        for patch in "${PATCHES[@]}"; do
            new_section="$new_section\nPatch${i}: $(basename "$patch")"
            i=$(( i + 1 ))
        done

        new_section="$new_section\n%endif"

        echo -e "$new_section" > "$TMP_TXT"
        # Pin the new section under Source0
        sed -i "/^Source0/r $TMP_TXT" "$output_path" || error "Failed to add new section to spec file!"

        # add changelog entry
        echo -e "* $(date +"%a %b %d %Y") Build Script <build-script@build.script> $DVER-1\n- Build new driver $DNAME-$DVER" > "$TMP_TXT"
        sed -i "/$regex_changelog/r $TMP_TXT" "$output_path" || error "Failed to add changelog entry to spec file!"
    fi

    rm -rf "$TMP_TXT"
}

# args:
#   1. use existing patches?
config_build_dir() {
    mkdir -p "$BUILD_DIR/SOURCES"

    [[ -n "$SRCTAR" ]] && cp "$SRCTAR" "$BUILD_DIR/SOURCES"
    mv "${SPEC_DIR}/${BUILD_SPEC}" "$BUILD_DIR"
    for file in $(find "$SPEC_DIR" -path "$BUILD_DIR" -prune -o -name "*" -print); do
        local base_fname="$(basename "$file")"
        if [[ -f "$file" ]] && [[ "${base_fname##*.}" != "spec" ]] && [[ ! "${base_fname#*.}" =~ spec.in$ ]]; then
            cp "$file" "$BUILD_DIR/SOURCES"
        fi
    done

    # this should be only for patches with paths,
    # i.e, patches that were specified on the cmdline
    # patches picked up from the spec file will be copied above anyways
    if [[ "$1" -eq 0 ]]; then
        for patch in "${PATCHES[@]}"; do
            [[ ! -f "$patch" ]] &&  error "Tried to find patch $patch but it doesn't exist!"
            cp "$patch" "$BUILD_DIR/SOURCES" || error "Failed to copy $patch to $BUILD_DIR/SOURCES!"
        done
    fi
}

clean_up() {
    rm -rf "$CUSTOM_TEMPLATE"
    rm -rf "$BUILD_DIR"
    rm -rf "$TMP_TXT"
}

main() {
    local base_template="$SPEC_DIR/kernels-drivers-intel-$DNAME.spec.in"
    local regex_str="^%if.*%{src_ver}.*==.*$DVER\"?$"
    # is this a new driver version? e.g not seen in spec file
    local is_new_dver=0
    # are we using the existing patches in the spec?
    local use_existing_patches=1
    local ret_val=

    # go to the main photon directory
    pushd "$SCRIPT_DIR/../../" &> /dev/null || error "Failed to push directory!"

    grep -Eq "$regex_str" "$base_template"
    ret_val="$?"
    if [[ "$ret_val" -eq 1 ]]; then
        is_new_dver=1
    elif [[ "$ret_val" -eq 2 ]]; then
        error "Failed to grep for existing versions in $base_template!"
    fi

    { [[ ${#PATCHES[@]} -gt 0 ]] || [[ $DISABLE_PATCHES -eq 1 ]]; } && use_existing_patches=0

    generate_custom_template "$base_template" \
                            "$CUSTOM_TEMPLATE" \
                            "$is_new_dver" \
                            "$use_existing_patches" \
                            "$DISABLE_PATCHES"

    KERNEL_VERSION="$KVER" source ./tools/scripts/create-kernel-deps-specs-from-template.sh

    # If we have to build custom template spec
    if [[ "$is_new_dver" -eq 1 ]] || [[ "$use_existing_patches" -eq 0 ]] || [[ ! -f "${BUILD_DIR}/${BUILD_SPEC}" ]]; then
        specs=( "$CUSTOM_TEMPLATE" )
        d_info["$DNAME"]="$DVER %{${DNAME^^}_VERSION}"

        echo "Creating custom driver spec for $DNAME-$DVER, kernel version=$KVER"
        create_specs "linux${KFLAV}"
    fi

    config_build_dir "$use_existing_patches"

    pushd "$BUILD_DIR" &> /dev/null || error "Failed to push directory"
    if ! "${SCRIPT_DIR}"/build_spec.sh "${BUILD_DIR}/${BUILD_SPEC}"; then
        error "Failed to build RPM!"
    fi
    popd &> /dev/null || error "Failed to popd"

    mkdir -p "$OUT_DIR"
    cp $(find "$BUILD_DIR/stage" -name "*.rpm") "$OUT_DIR" || exit 1
    echo "Moved driver RPMs from temporary location $BUILD_DIR/stage to $OUT_DIR"
    popd &> /dev/null || error "Failed to popd"
}

trap clean_up SIGINT SIGTERM EXIT

parse_args "$@"

main

clean_up