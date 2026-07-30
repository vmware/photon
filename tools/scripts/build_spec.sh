#! /bin/bash

BUILD_SCRIPT_VERSION=1.4

# Target to Photon OS version
VERSION="5.0"

# Subrelease
SUBRELEASE=""

# Target Photon OS docker image (if different than `photon:<version>`)
DKR_IMG=""
[[ -z "$DKR_IMG" ]] && DKR_IMG="photon:$VERSION"

# Keep running container instance alive?
KEEP_SANDBOX_AFTER_FAILURE=1

# Draw spinner while waiting
DRAW_SPINNER=1

# Process %check section
WITH_CHECK=0

# Array of rpmbuild/rpmspec macro definitions
# Example: RPM_MACROS=( --define \"vmxnet3_sw_timestamp 1\" )
RPM_MACROS=()

# Local path to a snapshot-<N>-Update<M>.<arch>.list (or plain package_list) file.
# When set, the sandbox is pinned to these exact package NVRs via tdnf's
# native `snapshot=` repo directive instead of resolving latest from the
# live photon repo, giving a reproducible build environment. Unlike
# VERSION/SUBRELEASE/DKR_IMG above, this has no static default to edit here:
# it names a specific file that necessarily changes per invocation, so it is
# only ever set via the --snapshot/-s flag parsed below.
SNAPSHOT_LIST=""

# Where the RPMs named in SNAPSHOT_LIST actually live. Accepts:
#   - an http(s)/ftp URL to a repo (e.g. an internal mirror or artifactory path)
#   - a local directory containing the RPMs (repo-formatted, with repodata/)
#   - "local", to source them from the same $STAGE_RPMS/LOCAL_RPMS dir already
#     mounted into the sandbox for the local repo, without a separate mirror
# Left empty, defaults to the official Broadcom Photon repo for $VERSION.
SNAPSHOT_BASEURL=""

# Only the official Broadcom repo (the SNAPSHOT_BASEURL-unset default) is
# signed with the Photon GPG key - mirrors/local directories/local RPMs are
# assumed unsigned unless proven otherwise. Set below once SNAPSHOT_BASEURL
# is resolved.
SNAPSHOT_GPGCHECK=0

TOPDIR="/usr/src/photon"
SRCDIR="$TOPDIR/SOURCES"
SNAPDIR="$TOPDIR/SNAPSHOT"
SNAP_BASEURL_DIR="$TOPDIR/SNAPSHOT_RPMS"

# Pull --snapshot/-s and --snapshot-baseurl/-b out of the argument list before
# positional parsing so they can appear anywhere:
# build_spec.sh <spec> [outdir] [--snapshot <file>] [--snapshot-baseurl <url-or-dir>]
# (CLI flags rather than more top-of-file variables, since a snapshot pin is
# per-invocation input, not a per-checkout setting like VERSION/SUBRELEASE.)
ARGS=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --snapshot=*)
      SNAPSHOT_LIST="${1#*=}"
      shift
      ;;
    --snapshot|-s)
      SNAPSHOT_LIST="$2"
      shift 2
      ;;
    --snapshot-baseurl=*)
      SNAPSHOT_BASEURL="${1#*=}"
      shift
      ;;
    --snapshot-baseurl|-b)
      SNAPSHOT_BASEURL="$2"
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done
set -- "${ARGS[@]}"

test "$#" -lt 1 && echo "Usage: $0 <spec-file-to-build.spec> [path-to-output-directory] [--snapshot <snapshot-list-file>] [--snapshot-baseurl <url-or-local-dir>]" && exit 1

CP="cp"
READLINK="readlink"

if [[ $OSTYPE = 'darwin'* ]]; then
  CP="gcp"
  READLINK="greadlink"

  export PATH=$PATH:"/opt/homebrew/bin"

  if ! $CP --version 2>&1 | grep -w coreutils; then
    echo -n '
You are running this script on MacOS

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Please install brew using above command. And do: $ brew install coreutils
GNU Tools are needed for this script to run properly.
'
    exit 1
  fi
fi

CONTAINER=build_spec
SOURCES_BASEURL=https://packages.broadcom.com/photon/photon_sources/1.0
SPECPATH=$($READLINK -m "$1")
SPECFILE=$(basename "$SPECPATH")
SPECDIR=$(dirname "$SPECPATH")

find_ph_root() {
  local cur_dir="$SPECDIR"

  # build-config.json is always present in the root directory
  while [ ! -e "${cur_dir}/build-config.json" ]; do
    cur_dir="$(dirname $cur_dir)"
    if [ "$cur_dir" == "/" ]; then
      cur_dir=""
      break
    fi
  done

  echo "$cur_dir"
}
PH_ROOT=$(find_ph_root)

# If not in a Photon repo, just use the spec parent directory as the root
[[ -z "$PH_ROOT" ]] && PH_ROOT="$SPECDIR"

STAGE_DIR="$(realpath ${PH_ROOT})/stage"
STAGE_SOURCES="$(realpath ${STAGE_DIR})/SOURCES"
STAGE_RPMS="$STAGE_DIR/RPMS"

# -v mount to inject into `docker run`, and the resulting baseurl= value
# written into the sandbox's [photon] repo when pinning to a snapshot.
# Populated below when a local SNAPSHOT_BASEURL directory is given; left
# empty for URLs (no mount needed).
BASEURL_MOUNT=""
SNAPSHOT_REPO_BASEURL=""

if [[ -n "$SNAPSHOT_LIST" ]]; then
  SNAPSHOT_LIST=$($READLINK -m "$SNAPSHOT_LIST")
  [[ ! -f "$SNAPSHOT_LIST" ]] && echo "Snapshot list not found: $SNAPSHOT_LIST" && exit 1

  if [[ -z "$SNAPSHOT_BASEURL" ]]; then
    # Default: official Broadcom Photon repo, matching the baseurl used by
    # the standard photon-snapshot.repo templates shipped with the OS.
    SNAPSHOT_REPO_BASEURL="https://packages.broadcom.com/photon/$VERSION/photon_${VERSION}_"'\$basearch'
    SNAPSHOT_GPGCHECK=1
  elif [[ "$SNAPSHOT_BASEURL" == "local" ]]; then
    # Reuse the local RPMs dir already mounted at $TOPDIR/LOCAL_RPMS for the
    # local repo, instead of requiring a separate mirror/baseurl/repo.
    SNAPSHOT_REPO_BASEURL="file://$TOPDIR/LOCAL_RPMS"
  elif [[ "$SNAPSHOT_BASEURL" =~ ^[a-zA-Z][a-zA-Z0-9+.-]*:// ]]; then
    # Any URL (internal mirror, artifactory, ftp, existing file:// path, etc.)
    SNAPSHOT_REPO_BASEURL="$SNAPSHOT_BASEURL"
  else
    # Local directory of RPMs (with repodata/) - mount it read-only into the
    # sandbox and point the repo at it via file://.
    SNAPSHOT_BASEURL=$($READLINK -m "$SNAPSHOT_BASEURL")
    [[ ! -d "$SNAPSHOT_BASEURL" ]] && echo "Snapshot baseurl directory not found: $SNAPSHOT_BASEURL" && exit 1
    BASEURL_MOUNT="-v $SNAPSHOT_BASEURL:$SNAP_BASEURL_DIR:ro"
    SNAPSHOT_REPO_BASEURL="file://$SNAP_BASEURL_DIR"
  fi

  # Tag the cached template image with the snapshot list + baseurl so
  # different sources/snapshots never share a template, while repeat builds
  # against the same pin still reuse it.
  CONTAINER_IMG="photon_build_spec:$VERSION-snapshot-$(echo "$SNAPSHOT_LIST|$SNAPSHOT_BASEURL" | md5sum | cut -c1-12)"
elif [[ -n "$SUBRELEASE" ]]; then
  CONTAINER_IMG="photon_build_spec:$VERSION-$SUBRELEASE"
else
  CONTAINER_IMG="photon_build_spec:$VERSION"
fi

DIST=".ph$(echo $VERSION | cut -d. -f1)"

if [ -z "$2" ]; then
  LOCAL_STAGE="$STAGE_DIR/$(cut -d '.' -f 1 <<<"$SPECFILE")"
else
  LOCAL_STAGE=$($READLINK -m "$2")
fi
LOCAL_SOURCES="${LOCAL_STAGE}/SOURCES"

if [ -e $LOCAL_STAGE ]; then
  rm -rf $LOCAL_STAGE
fi

mkdir -p ${LOCAL_STAGE}/{LOGS,RPMS,SRPMS,SNAPSHOT} \
         $LOCAL_SOURCES \
         $STAGE_SOURCES \
         $STAGE_RPMS

LOCAL_SNAPSHOT_DIR="${LOCAL_STAGE}/SNAPSHOT"
if [[ -n "$SNAPSHOT_LIST" ]]; then
  cp "$SNAPSHOT_LIST" "${LOCAL_SNAPSHOT_DIR}/snapshot.list"
fi

LOGFILE=${LOCAL_STAGE}/LOGS/$(basename "$SPECFILE" .spec).log

RPM_MACROS+=( --define \"dist $DIST\" --define \"with_check $WITH_CHECK\" )

# use &3 for user output
exec 3>&1
# redirect &1 and &2 to the log file
exec &>"$LOGFILE"

# First argument meaning: 1 - exit on fail, 0 - continue on failure.
wait_for_result() {
  local pid=$!
  if [ "$DRAW_SPINNER" -eq 1 ]; then
    local spin='-\|/'
    local i=0
    echo -n " " >&3
    while [ -d /proc/$pid ]; do
      sleep .25
      echo -ne "\b${spin:i++%4:1}" >&3
    done
    echo -ne "\b" >&3
  fi
  if wait $pid; then
    echo -e "\033[0;32mOK\033[0m" >&3
  elif [ $1 -eq 0 ]; then
    echo -e "\033[0;33mERROR\033[0m" >&3
    return 1
  else
    echo -e "\033[0;31mFAIL\033[0m" >&3
    fail
  fi
  return 0
}

run() {
  echo -ne "\t$1 " >&3
  shift
  echo "run: $*"
  "$@" &
  wait_for_result 1
}

tryrun() {
  echo -ne "\t$1 " >&3
  shift
  echo "run: $*"
  "$@" &
  wait_for_result 0
}

in_sandbox() {
  eval docker exec --privileged ${CONTAINER} $@
}

create_sandbox() {
  docker ps -f "name=$CONTAINER" && docker rm -f $CONTAINER
  docker inspect --format='{{.Created}}' $CONTAINER_IMG
  local status=$?
  local cdate
  cdate=$(date --date="$(docker inspect --format='{{.Created}}' $CONTAINER_IMG)" '+%s')
  # image exists?
  if [ $status -eq 0 ]; then
    local vdate
    vdate=$(($(date '+%s') - 1209600))
    # image is less then 2 weeks
    if [ "$cdate" -gt "$vdate" ]; then
      # use this image
      run "Use local build template image" \
        docker run --ulimit nofile=1024:1024 \
        -v ${LOCAL_SOURCES}:$SRCDIR \
        -v $LOCAL_STAGE/RPMS:$TOPDIR/RPMS \
        -v $LOCAL_STAGE/SRPMS:$TOPDIR/SRPMS \
        -v $STAGE_RPMS:$TOPDIR/LOCAL_RPMS \
        -v $LOCAL_SNAPSHOT_DIR:$SNAPDIR \
        $BASEURL_MOUNT \
        --privileged -d --name $CONTAINER --network="host" \
        $CONTAINER_IMG tail -f /dev/null
      return 0
    fi
    # remove old image
    docker image rm $CONTAINER_IMG
  fi

  run "Pull photon image" \
    docker run --ulimit nofile=1024:1024 \
    -v ${LOCAL_SOURCES}:$SRCDIR \
    -v $LOCAL_STAGE/RPMS:$TOPDIR/RPMS \
    -v $LOCAL_STAGE/SRPMS:$TOPDIR/SRPMS \
    -v $STAGE_RPMS:$TOPDIR/LOCAL_RPMS \
    -v $LOCAL_SNAPSHOT_DIR:$SNAPDIR \
    $BASEURL_MOUNT \
    --privileged -d --name $CONTAINER --network="host" \
    "$DKR_IMG" tail -f /dev/null

  # replace toybox with coreutils and install default build tools
  run "Replace toybox with coreutils" in_sandbox tdnf remove -y toybox

  run "Upgrade Packages" in_sandbox tdnf upgrade --refresh -y

  run "Install default build tools" \
    in_sandbox tdnf install -y rpm-build build-essential gmp-devel \
      mpfr-devel tar sed findutils file gzip patch bzip2 createrepo python3

  in_sandbox "mkdir -p $TOPDIR/LOCAL_RPMS"

  run "Create local repo in sandbox" echo -e "[local]\nname=VMWare Photon Linux Local\nbaseurl=file://$TOPDIR/LOCAL_RPMS\nenabled=1\ngpgcheck=0\nskip_if_unavailable=1\npriority=10" | sed 1d | docker exec -i $CONTAINER sh -c 'cat > /etc/yum.repos.d/local.repo'

  if [[ -n "$SNAPSHOT_LIST" ]]; then
    # Disable every default repo (now including the local repo just created
    # above) so the snapshot pin below ends up the only enabled repo - no
    # priority=10 local repo left that could silently win over the pin.
    run "Disable default repos for snapshot pin" \
      docker exec -i $CONTAINER sh -c "sed -i 's/^enabled=1/enabled=0/' /etc/yum.repos.d/*.repo"

    # Re-point the existing [photon] repo at the snapshot instead of writing
    # a whole new repo file from scratch, so it keeps the real gpgkey list
    # and other fields already shipped with the image.
    local snapshot_repo_tmp
    snapshot_repo_tmp=$(mktemp)
    docker cp "$CONTAINER:/etc/yum.repos.d/photon.repo" "$snapshot_repo_tmp"
    sed -i \
      -e "s|^baseurl=.*|baseurl=$SNAPSHOT_REPO_BASEURL|" \
      -e "/^baseurl=/a snapshot=file://$SNAPDIR/snapshot.list" \
      -e "s/^gpgcheck=.*/gpgcheck=$SNAPSHOT_GPGCHECK/" \
      -e "s/^enabled=.*/enabled=1/" \
      "$snapshot_repo_tmp"
    run "Pin sandbox to snapshot $(basename "$SNAPSHOT_LIST")" \
      docker cp "$snapshot_repo_tmp" "$CONTAINER:/etc/yum.repos.d/photon.repo"
    rm -f "$snapshot_repo_tmp"
  fi

  run "Create build template image for future use" docker commit "$(docker ps -q -f "name=$CONTAINER")" $CONTAINER_IMG
}

prepare_buildenv() {
  local file=
  local url=
  local enable_photon=

  [[ -z "$SUBRELEASE" && -z "$SNAPSHOT_LIST" ]] && enable_photon="--enablerepo photon"

  in_sandbox mkdir -p $SRCDIR

  echo "Copy sources from $SPECDIR"
  for f in $(find $SPECDIR -name "*"); do
    copy_spec_srcs "$f"
  done

  for url in $(in_sandbox rpmspec ${RPM_MACROS[@]} -P $SRCDIR/"$SPECFILE" | grep "Source[[:digit:]]*:" | grep -o '[^[:space:]]\+$'); do
    file=$(basename "$url")
    local spec_source="$SPECDIR/$file"

    test -e "$LOCAL_SOURCES/$file" && continue

    in_sandbox "ls -l $SRCDIR"

    local stage_source="${STAGE_SOURCES}/${file}"
    if [ ! -e "$stage_source" ]; then
      tryrun "Download $file" wget "$SOURCES_BASEURL/$file" -O "${stage_source}"
      # Retry from original URL
      [ $? -eq 0 ] || run "Download $url" wget "$url" -O "${stage_source}"
    fi

    run "Create hard link for source tarball $stage_source" ln $stage_source $LOCAL_SOURCES
  done

  run "createrepo" in_sandbox "createrepo --update --general-compress-type=gz $TOPDIR/LOCAL_RPMS"
  run "makecache" in_sandbox "tdnf makecache --refresh"

  local br
  br=$(in_sandbox rpmspec ${RPM_MACROS[@]} -P $SRCDIR/"$SPECFILE" | sed -n 's/^BuildRequires://p' | sed 's/ \(<\|\)= /=/g;s/>\(=\|\) [^ ]*//g;s/ \+/ /g' | tr '\n' ' ')
  if [ -n "$br" ]; then
    run "Install build requirements" in_sandbox tdnf install -y $enable_photon --refresh $br
  fi
}

build() {
  echo -ne "\tRun rpmbuild " >&3
  [ $WITH_CHECK -eq 0 ] && WITH_CHECK_PARAM="--nocheck"
  in_sandbox rpmbuild $WITH_CHECK_PARAM -ba ${RPM_MACROS[@]} $SRCDIR/"$SPECFILE" &
  wait_for_result 1
  run "Delete SOURCES" rm -rf $LOCAL_SOURCES
}

destroy_sandbox() {
  run "Stop container" docker kill $CONTAINER
  run "Remove container" docker rm $CONTAINER
}

clean_up() {
  echo "Post clean up" >&3
  docker ps -f "name=$CONTAINER" &>/dev/null && destroy_sandbox &>/dev/null
}

fail() {
  test "$KEEP_SANDBOX_AFTER_FAILURE" -ne 1 && clean_up || \
    echo "Sandbox is preserved for analisys. Use 'docker exec -it $CONTAINER /bin/bash'" >&3
  echo "Build failed. See $LOGFILE for full output" >&3
  echo -e "\033[1;33m" >&3
  tail "$LOGFILE" >&3
  echo -e "\033[0m" >&3
  exit 1
}

copy_spec_srcs() {
  [[ ! -f "$1" ]] && return 0
  [[ -f "${LOCAL_SOURCES}/$(basename $1)" ]] && return 0

  ln "$1" "${LOCAL_SOURCES}" || fail
}

trap clean_up SIGINT SIGTERM

echo "0. Build Script Version:" $BUILD_SCRIPT_VERSION >&3

echo "1. Create sandbox" >&3
create_sandbox

echo "2. Prepare build environment" >&3
prepare_buildenv

echo "3. Build Binary and Source Package" >&3
build

echo "4. Destroy sandbox" >&3
destroy_sandbox

echo "Build completed. RPMS are in '$LOCAL_STAGE' folder" >&3
