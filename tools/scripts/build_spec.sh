#! /bin/bash

BUILD_SCRIPT_VERSION=1.1

# Target to Photon OS version
VERSION=5

# Keep running container instance alive?
KEEP_SANDBOX_AFTER_FAILURE=1

# Draw spinner while waiting
DRAW_SPINNER=1

# Process %check section
WITH_CHECK=0

# Array of rpmbuild/rpmspec macro definitions
# Example: RPM_MACROS=( --define \"vmxnet3_sw_timestamp 1\" )
RPM_MACROS=()

test "$#" -lt 1 && echo "Usage: $0 <spec-file-to-build.spec> [path-to-output-directory]" && exit 1

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
SOURCES_BASEURL=https://packages.vmware.com/photon/photon_sources/1.0
SPECPATH=$($READLINK -m "$1")
SPECFILE=$(basename "$SPECPATH")
SPECDIR=$(dirname "$SPECPATH")

if [ -z "$2" ]; then
  STAGE="$SPECDIR/stage"
else
  STAGE=$($READLINK -m "$2")
fi

mkdir -p ${STAGE}/LOGS
LOGFILE=stage/LOGS/$(basename "$SPECFILE" .spec).log

RPM_MACROS+=( --define \"dist .ph$VERSION\" --define \"with_check $WITH_CHECK\" )

mkdir -p ${STAGE}/{RPMS,SRPMS}

# use &3 for user output
exec 3>&1
# redirect &1 and &2 to the log file
exec &>"$LOGFILE"

# First argument meaning: 1 - exit on fail, 0 - continue on failure.
function wait_for_result() {
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

function run() {
  echo -ne "\t$1 " >&3
  shift
  echo "run: $*"
  "$@" &
  wait_for_result 1
}

function tryrun() {
  echo -ne "\t$1 " >&3
  shift
  echo "run: $*"
  "$@" &
  wait_for_result 0
}

function in_sandbox() {
  eval docker exec --privileged ${CONTAINER} $@
}

function create_sandbox() {
  docker ps -f "name=$CONTAINER" && docker rm -f $CONTAINER
  docker inspect --format='{{.Created}}' photon_build_spec:$VERSION.0
  local status=$?
  local cdate
  cdate=$(date --date="$(docker inspect --format='{{.Created}}' photon_build_spec:$VERSION.0)" '+%s')
  # image exists?
  if [ $status -eq 0 ]; then
    local vdate
    vdate=$(($(date '+%s') - 1209600))
    # image is less then 2 weeks
    if [ "$cdate" -gt "$vdate" ]; then
      # use this image
      run "Use local build template image" docker run --ulimit nofile=1024:1024 -v $STAGE/RPMS:/usr/src/photon/RPMS -v $STAGE/SRPMS:/usr/src/photon/SRPMS --privileged -d --name $CONTAINER --network="host" photon_build_spec:$VERSION.0 tail -f /dev/null
      return 0
    else
      # remove old image
      docker image rm photon_build_spec:$VERSION.0
    fi
  fi


  run "Pull photon image" docker run --ulimit nofile=1024:1024 -v $STAGE/RPMS:/usr/src/photon/RPMS -v $STAGE/SRPMS:/usr/src/photon/SRPMS --privileged -d --name $CONTAINER --network="host" photon:$VERSION.0 tail -f /dev/null

  # replace toybox with coreutils and install default build tools
  run "Replace toybox with coreutils" in_sandbox tdnf remove -y toybox
  run "Upgrade Packages" in_sandbox tdnf upgrade -y
  run "Install default build tools" in_sandbox tdnf install -y rpm-build build-essential gmp-devel mpfr-devel tar sed findutils file gzip patch bzip2 createrepo python3
  run "Create local repo in sandbox" echo -e "[local]\nname=VMWare Photon Linux Local\nbaseurl=file:///usr/src/photon/RPMS\nenabled=1\nskip_if_unavailable=1" | sed 1d | docker exec -i $CONTAINER sh -c 'cat > /etc/yum.repos.d/local.repo'

  run "Create build template image for future use" docker commit "$(docker ps -q -f "name=$CONTAINER")" photon_build_spec:$VERSION.0
}

function prepare_buildenv() {
  mkdir -p "$SPECDIR/SOURCES"
  in_sandbox mkdir -p /usr/src/photon/SOURCES
  run "Create source folder" find "$SPECDIR" -type f -exec $CP -u {} "$SPECDIR/SOURCES" \;
  run "Copy sources from $SPECDIR" docker cp "$SPECDIR/SOURCES/." $CONTAINER:/usr/src/photon/SOURCES

  for url in $(in_sandbox rpmspec ${RPM_MACROS[@]} -P /usr/src/photon/SOURCES/"$SPECFILE" | grep "Source[[:digit:]]*:" | grep -o '[^[:space:]]\+$');
  do
    file=$(basename "$url")
    test -f "$SPECDIR/SOURCES/$file" && continue
    tryrun "Download $file" wget "$SOURCES_BASEURL/$file" -O "$SPECDIR/SOURCES/$file" && docker cp "$SPECDIR/SOURCES/$file" $CONTAINER:/usr/src/photon/SOURCES
    # Retry from original URL
    [ $? -eq 0 ] || run "Download $url" wget "$url" -O "$SPECDIR/SOURCES/$file" && docker cp "$SPECDIR/SOURCES/$file" $CONTAINER:/usr/src/photon/SOURCES
  done

  run "createrepo " in_sandbox createrepo /usr/src/photon/RPMS/.
  run "makecache" in_sandbox tdnf makecache

  local br
  br=$(in_sandbox rpmspec ${RPM_MACROS[@]} -P /usr/src/photon/SOURCES/"$SPECFILE" | sed -n 's/BuildRequires://p' | sed 's/ \(<\|\)= /=/g;s/>\(=\|\) [^ ]*//g;s/ \+/ /g' | tr '\n' ' ')
  if [ "$br" != "" ]; then
    run "Install build requirements" in_sandbox tdnf install -y --enablerepo photon $br
  fi
}

function build() {
  echo -ne "\tRun rpmbuild " >&3
  [ $WITH_CHECK -eq 0 ] && WITH_CHECK_PARAM="--nocheck"
  in_sandbox rpmbuild $WITH_CHECK_PARAM -ba ${RPM_MACROS[@]} /usr/src/photon/SOURCES/"$SPECFILE" &
  wait_for_result 1
  run "Delete SOURCES" rm -rf $SPECDIR/SOURCES
}

function destroy_sandbox() {
  run "Stop container" docker kill $CONTAINER
  run "Remove container" docker rm $CONTAINER
}

function clean_up() {
  echo "Post clean up" >&3
  docker ps -f "name=$CONTAINER" &>/dev/null && destroy_sandbox &>/dev/null
}

function fail() {
  test "$KEEP_SANDBOX_AFTER_FAILURE" -ne 1 && clean_up || \
    echo "Sandbox is preserved for analisys. Use 'docker exec -it $CONTAINER /bin/bash'" >&3
  echo "Build failed. See $LOGFILE for full output" >&3
  echo -e "\033[1;33m" >&3
  tail "$LOGFILE" >&3
  echo -e "\033[0m" >&3
  exit 1
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

echo "Build completed. RPMS are in '$STAGE' folder" >&3
