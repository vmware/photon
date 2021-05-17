#! /bin/bash
#
# Canister buider. It uses rpmbuild inside Photon docker image.
#
# Copyright (C) 2020, 2021, VMware, Inc.
# Authors: Keerthana Kalyanasundaram <keerthanak@vmware.com>
#          Alexey Makhalov <amakhalov@vmware.com>
#



# Target to Photon OS version
VERSION=4

# Keep running container instance alive?
KEEP_SANDBOX_AFTER_FAILURE=1

# Draw spinner while waiting
DRAW_SPINNER=1

# Build vmlinux and modules (1) or canister only (0)
# Using FULL_BUILD=0 can be usefull during canister development
# stage, but should not be used for production build as it skips
# important step - final linking into vmlinux.
FULL_BUILD=0

# Use local patches/0001-FIPS-canister-binary-usage.patch instead of
# original patch from github.
OVERWRITE_CANISTER_USAGE_PATCH=0

# Set this flag to 1, to build with broken kat tests
KATBUILD=0

test "$#" -ne 1 -o "${1:0:5}" != "linux" && echo "Usage: $0 Linux flavour to build (e.g: linux / linux-secure)" && exit 1

CONTAINER=build_spec
FLAVOR=${1:6}
CANISTER_SOURCE_VERSION=4.0.1
CANISTER_FULL_VERSION="LKCM $CANISTER_SOURCE_VERSION"
CANISTER_TARBALL_VERSION=""
KERNEL_VERSION=""
CURDIR=`pwd`
SPECPATH=$CURDIR/build/linux/$1.spec
SPECFILE=$1.spec
SPECDIR=$CURDIR/build/linux
BUILDDIR=$CURDIR/build
PATCHDIR=$CURDIR/patches
SRCDIR=$CURDIR/crypto
mkdir -p $SPECDIR
mkdir -p $BUILDDIR/stage/LOGS
mkdir -p $BUILDDIR/stage/{tmp,canister-binaries}
TMPFOLDER=$BUILDDIR/stage/tmp/
LOGFILE=$BUILDDIR/stage/LOGS/$(basename $SPECFILE .spec).log

# use &3 for user output
exec 3>&1
# redirect &1 and &2 to the log file
exec &>$LOGFILE

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
  wait $pid
  if [ $? -eq 0 ]; then
    echo -e "\033[0;32mOK\033[0m" >&3
  else
    echo -e "\033[0;31mFAIL\033[0m" >&3
    fail
  fi
}

function run() {
  echo -ne "\t$1 " >&3
  shift
  echo "run: $@"
  $@ &
  wait_for_result
}

function in_sandbox() {
  docker exec $CONTAINER "$@"
}

function download_spec_patches() {
    rm -rf photon
    git clone --depth 1 --single-branch --branch 4.0 https://github.com/vmware/photon.git
#    mkdir photon
#    cp -r ~/gerrit/photon/SPECS/ photon/
}

function copy_photon_sources_patches() {
    find photon/SPECS/linux -mindepth 1 -type f -exec cp -t $SPECDIR/ {} +
    version=$(grep "Version:" $SPECPATH | awk '{print $2}')
    release=$(grep "Release:" $SPECPATH | awk '{print $2}' | cut -d% -f1)
    KERNEL_VERSION="$version-$release"
    CONF_FILE=$SPECDIR/config-$FLAVOR
    # Make path relative (patch friendly)
    test -z "$FLAVOR" && CONF_FILE=${SPECDIR:${#CURDIR} + 1}/config_x86_64

    if [[ "$FLAVOR" = "secure" ]]; then
       KERNEL_VERSION="$KERNEL_VERSION-$FLAVOR"
       # Do not check for lists corruption in the canister.
       sed -i "s/CONFIG_DEBUG_LIST=y/# CONFIG_DEBUG_LIST is not set/" $CONF_FILE
       sed -i "s/CONFIG_BUG_ON_DATA_CORRUPTION=y/# CONFIG_BUG_ON_DATA_CORRUPTION is not set/" $CONF_FILE
       # Disable struct layout randomization
       sed -i "s/CONFIG_GCC_PLUGIN_RANDSTRUCT=y/# CONFIG_GCC_PLUGIN_RANDSTRUCT is not set/" $CONF_FILE
       sed -i "/CONFIG_GCC_PLUGIN_RANDSTRUCT_PERFORMANCE=y/d" $CONF_FILE
       sed -i "/# CONFIG_DEBUG_INFO_DWARF4 is not set/a  # CONFIG_DEBUG_INFO_BTF is not set" $CONF_FILE
    else
	# Enable strong stack protector
       sed -i "s/# CONFIG_STACKPROTECTOR_STRONG is not set/CONFIG_STACKPROTECTOR_STRONG=y/" $CONF_FILE
	# Enable stack leak protection
	patch -p0 << EOF
--- $CONF_FILE       2021-03-08 14:30:06.420672563 -0800
+++ $CONF_FILE.new     2021-03-08 14:30:42.916893895 -0800
@@ -6055,14 +6055,16 @@
 #
 # Kernel hardening options
 #
+CONFIG_GCC_PLUGIN_STRUCTLEAK=y

 #
 # Memory initialization
 #
-CONFIG_INIT_STACK_NONE=y
+# CONFIG_INIT_STACK_NONE is not set
 # CONFIG_GCC_PLUGIN_STRUCTLEAK_USER is not set
 # CONFIG_GCC_PLUGIN_STRUCTLEAK_BYREF is not set
-# CONFIG_GCC_PLUGIN_STRUCTLEAK_BYREF_ALL is not set
+CONFIG_GCC_PLUGIN_STRUCTLEAK_BYREF_ALL=y
+# CONFIG_GCC_PLUGIN_STRUCTLEAK_VERBOSE is not set
 # CONFIG_GCC_PLUGIN_STACKLEAK is not set
 # CONFIG_INIT_ON_ALLOC_DEFAULT_ON is not set
 # CONFIG_INIT_ON_FREE_DEFAULT_ON is not set
EOF
    fi
    CANISTER_TARBALL_VERSION="$CANISTER_SOURCE_VERSION-$KERNEL_VERSION"
    wget https://packages.vmware.com/photon/photon_sources/1.0/linux-$version.tar.xz -P $SPECDIR/
    
    grep "Source.*:" $SPECPATH | awk '{print $2}' | while read -r line ; do
       if [[ $line =~ "tar" ]]; then
          if [[ $line =~ "%{" ]]; then
             if ! [[ $line =~ "%{version}" ]]; then
                  versionvar=$(echo $line | sed -n "s/^.*%{\s*\(\S*\).*$/\1/p" | cut -d } -f 1)
                  versionval=$(grep "$versionvar " $SPECPATH | awk '{print $3}')
                  version="\%\{$versionvar\}"
                  pkgname="$(basename $line)"
                  name="${pkgname/$version/$versionval}"
                  wget https://packages.vmware.com/photon/photon_sources/1.0/$name -P $SPECDIR/
             fi
          else
            name=$(basename $line)
            wget https://packages.vmware.com/photon/photon_sources/1.0/$name -P $SPECDIR
          fi
       fi
    done
}

function copy_and_apply_canister_patch() {
  if [ "$OVERWRITE_CANISTER_USAGE_PATCH" -eq 1 ]; then
    cp $PATCHDIR/0001-FIPS-canister-binary-usage.patch $SPECDIR
  fi

  patchname="0002-FIPS-canister-creation.patch"
  srcpatchname="canister-src-$CANISTER_SOURCE_VERSION.patch"
  if [[ "$FLAVOR" = "secure" ]]; then
     # Disable RAP HASH creation for AES-NI asm code
     flavor_patchname=$PATCHDIR/`basename $patchname .patch`-secure.patch
  else
     # Enable RAP plugin
     flavor_patchname=$PATCHDIR/`basename $patchname .patch`-non-secure.patch
  fi

  echo "Creating canister source files from $SRCDIR as patch"
  diff -Naur crypto-tmp/ crypto/ > "$srcpatchname"

  echo "Updating Canister version $CANISTER_FULL_VERSION in $SRCDIR/fips_integrity.c"
  sed -i "0,/FIPS_CANISTER_VERSION.*$/s/FIPS_CANISTER_VERSION.*$/FIPS_CANISTER_VERSION \"${CANISTER_FULL_VERSION}\"/" "$srcpatchname"

  echo "Updating Kernel version $KERNEL_VERSION in $SRCDIR/fips_integrity.c"
  sed -i "0,/FIPS_KERNEL_VERSION.*$/s/FIPS_KERNEL_VERSION.*$/FIPS_KERNEL_VERSION \"${KERNEL_VERSION}\"/" "$srcpatchname"

  echo "Copying patches to $SPECDIR"
  mv "$CURDIR/$srcpatchname" $SPECDIR
# Can be used later. Keep it around
#  cat "$PATCHDIR/$patchname" $flavor_patchname $PATCHDIR/crypto-Makefile-generate-ii-files.patch > $SPECDIR/$patchname
  cat "$PATCHDIR/$patchname" $flavor_patchname > $SPECDIR/$patchname

  echo "Adding fips-canister subpackage and patch to $SPECPATH"
  if [ "$KATBUILD" -eq 1 ]; then
     sed -i "/%global fips 1/a %global kat_build" $SPECPATH
  fi
  sed -i "/%global fips 1/d" $SPECPATH
  sed -i '0,/BuildRequires:/!b;//i\
Patch10000:     '${srcpatchname}'\
Patch10001:     0001-FIPS-canister-binary-usage.patch\
Patch10002:     '${patchname}'\
' $SPECPATH
  sed -i '0,/%build/!b;//i\
%patch10000 -p0\
%patch10001 -p1\
%patch10002 -p1\
chmod 750 crypto/update_canister_hmac.sh' $SPECPATH

  sed -i '0,/%prep/!b;//i\%package fips-canister \
Summary:        Photon FIPS canister binaries\
Group:          Development/libraries\
\
\%description fips-canister\
This package contains the fips canister binary.\
' $SPECPATH
  if [ "$FULL_BUILD" -eq 0 ]; then
    # No debuginfo
    sed -i '1i %define debug_package %{nil}' $SPECPATH
    # Remove all subpackages
    sed -i '/%package devel/,/%package fips-canister/{/%package fips-canister/!d}' $SPECPATH
    # Make crypto folder only and exit
    sed -i 's/make V=1/make V=1 crypto\/fips_canister.o/' $SPECPATH
    sed -i '/make V=1/a touch debugfiles.list\nexit 0' $SPECPATH
    # Stop on install, canister installation code will be inserted in between
    sed -i '/%install/a exit 0' $SPECPATH
    # Remove packaging and post sections
    sed -i '/%post/,/%changelog/{/%changelog/!d}' $SPECPATH
    sed -i '0,/%changelog/!b;//i\%files\
%defattr(-,root,root)\
' $SPECPATH
  fi
  sed -i '/%install/a install -vdm 755 \%{buildroot}\/usr\/lib\/fips-canister\/\
pushd crypto/\
mkdir fips-canister-'${CANISTER_TARBALL_VERSION}'\
cp fips_canister.o fips-canister-'${CANISTER_TARBALL_VERSION}'\
cp fips_canister_wrapper.c fips-canister-'${CANISTER_TARBALL_VERSION}'\
tar -cvjf fips-canister-'${CANISTER_TARBALL_VERSION}'.tar.bz2 fips-canister-'${CANISTER_TARBALL_VERSION}'/\
popd\
cp crypto\/fips-canister-'${CANISTER_TARBALL_VERSION}'.tar.bz2 \%{buildroot}\/usr\/lib\/fips-canister\/\
' $SPECPATH
  sed -i '0,/%changelog/!b;//i\%files fips-canister\
%defattr(-,root,root)\
\/usr\/lib\/fips-canister\/*\
' $SPECPATH
}

function create_sandbox() {
  docker ps -f "name=$CONTAINER" && docker rm -f $CONTAINER
  docker inspect --format='{{.Created}}' photon_build_spec:$VERSION
  local status=$?
  local cdate=$(date --date=`docker inspect --format='{{.Created}}' photon_build_spec:$VERSION` '+%s')
  # image exists?
  if [ $status -eq 0 ]; then
    local vdate=$((`date '+%s'` - 1209600))
    # image is less then 2 weeks
    if [ $cdate -gt $vdate ]; then
      # use this image
      run "Use local build template image" docker run -d --name $CONTAINER --network="host" photon_build_spec:$VERSION tail -f /dev/null
      return 0
    else
      # remove old image
      docker image rm photon_build_spec:$VERSION
    fi
  fi


  run "Pull photon image" docker run -d --name $CONTAINER --network="host" photonos-docker-local.artifactory.eng.vmware.com/photon$VERSION:20201120 tail -f /dev/null

  # replace toybox with coreutils and install default build tools
  run "Replace toybox with coreutils" in_sandbox tdnf remove -y toybox
  run "Install default build tools" in_sandbox tdnf install -y rpm-build build-essential tar sed findutils file gzip patch

  run "Create build template image for future use" docker commit `docker ps -q -f "name=$CONTAINER"` photon_build_spec:$VERSION
}

function prepare_buildenv() {
  run "Create source folder" in_sandbox mkdir -p /usr/src/photon/SOURCES
  run "Copy sources from $SPECDIR" docker cp $SPECDIR/. $CONTAINER:/usr/src/photon/SOURCES
  local br=`sed -n 's/^BuildRequires://p' $SPECPATH | sed 's/ \(<\|\)= /=/g;s/>\(=\|\) [^ ]*//g'`
  if [ "$br" != "" ]; then
    run "Install build requirements" in_sandbox tdnf install -y $br glibc-tools zlib-devel bzip2 bzip2-devel gettext util-linux util-linux-devel flex-devel readline-devel popt-devel nspr-devel texinfo lua-devel python3-xml libselinux glibc-iconv gmp-devel mpfr-devel sqlite nss nss-devel elfutils-devel libpipeline libdb-devel cpio
  fi
}

function build() {
  echo -ne "\tRun rpmbuild " >&3
  docker exec $CONTAINER rpmbuild -bb --define "dist .ph$VERSION" /usr/src/photon/SOURCES/$SPECFILE &
  wait_for_result
}

function get_rpms() {
  run "Copy RPMS" docker cp $CONTAINER:/usr/src/photon/RPMS $BUILDDIR/stage
  run "Copy SRPMS" docker cp $CONTAINER:/usr/src/photon/SRPMS $BUILDDIR/stage
}

function create_canister_tarball() {
  cp $BUILDDIR/stage/RPMS/x86_64/linux-*fips-canister*.rpm $TMPFOLDER
  pushd $TMPFOLDER && rpm2cpio linux-*fips-canister* | cpio -idmv && cp ./usr/lib/fips-canister/fips-canister-$CANISTER_TARBALL_VERSION.tar.bz2 $BUILDDIR/stage/canister-binaries && popd
}

function destroy_sandbox() {
  run "Stop container" docker kill $CONTAINER
  run "Remove container" docker rm $CONTAINER
  run "Clean up tmp folder" rm -rf $TMPFOLDER
  run "Clean up photon workspace" rm -rf photon/
}

function clean_build_env() {
  echo "Clean up build environment" >&3
  rm -rf photon/ $TMPFOLDER
}

function clean_up() {
  echo "Post clean up" >&3
  docker ps -f "name=$CONTAINER" &>/dev/null && destroy_sandbox && clean_build_env &>/dev/null
}

function fail() {
  test "$KEEP_SANDBOX_AFTER_FAILURE" -ne 1 && clean_up || \
    echo "Sandbox is preserved for analisys. Use 'docker exec -it $CONTAINER /bin/bash'" >&3
  echo "Build failed. See $LOGFILE for full output" >&3
  echo -e "\033[1;33m" >&3
  tail $LOGFILE >&3
  echo -e "\033[0m" >&3
  exit 1
}

trap clean_up SIGINT SIGTERM

echo "1. Download Photon sources" >&3
download_spec_patches

echo "2. Copy photon spec, sources and patches to build folder" >&3
copy_photon_sources_patches

echo "3. Copy canister patch and modify spec file" >&3
copy_and_apply_canister_patch

echo "4. Create sandbox" >&3
create_sandbox

echo "5. Prepare build environment" >&3
prepare_buildenv

echo "6. Build" >&3
build

echo "7. Get binaries" >&3
get_rpms

echo "8. Create canister tarball" >&3
create_canister_tarball

echo "8. Destroy sandbox" >&3
destroy_sandbox

echo "Build completed. RPMS are in '$BUILDDIR/stage' folder" >&3

