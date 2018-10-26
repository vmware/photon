#!/bin/bash

TOP_DIR_PATH=/usr/src/photon

function get_chroot_path()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_name=$pkg_name-$version
    local chroot_path=$src_root/stage/photonroot/$chroot_name
    echo $chroot_path
}

function __install_toolchain_rpms()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    TOOLCHAIN_PKGS=( \
       "filesystem" \
       "linux-api-headers" \
       "glibc" \
       "glibc-devel" \
       "glibc-iconv" \
       "glibc-tools" \
       "glibc-i18n" \
       "glibc-lang" \
       "zlib" \
       "zlib-devel" \
       "file-libs" \
       "file" \
       "binutils" \
       "binutils-devel" \
       "gmp" \
       "gmp-devel" \
       "mpfr" \
       "mpfr-devel" \
       "mpc" \
       "libgcc" \
       "libgcc-devel" \
       "libgcc-atomic" \
       "libstdc++" \
       "libstdc++-devel" \
       "libgomp" \
       "libgomp-devel" \
       "autoconf" \
       "automake" \
       "libtool" \
       "gcc" \
       "pkg-config" \
       "ncurses" \
       "ncurses-libs" \
       "ncurses-devel" \
       "bash" \
       "bzip2" \
       "bzip2-libs" \
       "bzip2-devel" \
       "sed" \
       "procps-ng" \
       "coreutils" \
       "m4" \
       "grep" \
       "readline" \
       "diffutils" \
       "gawk" \
       "findutils" \
       "gettext" \
       "gzip" \
       "make" \
       "patch" \
       "util-linux" \
       "util-linux-libs" \
       "util-linux-devel" \
       "tar" \
       "xz" \
       "xz-libs" \
       "flex" \
       "flex-devel" \
       "bison" \
       "readline-devel" \
       "lua" \
       "lua-devel" \
       "popt" \
       "popt-devel" \
       "nspr" \
       "nspr-devel" \
       "sqlite" \
       "sqlite-libs" \
       "nss" \
       "nss-libs" \
       "nss-devel" \
       "elfutils-libelf" \
       "elfutils" \
       "elfutils-libelf-devel" \
       "elfutils-devel" \
       "expat" \
       "expat-libs" \
       "libffi" \
       "libpipeline" \
       "gdbm" \
       "perl" \
       "texinfo" \
       "openssl" \
       "openssl-devel" \
       "python2" \
       "python2-libs" \
       "python2-devel" \
       "libcap" \
       "libdb" \
       "libdb-devel" \
       "rpm" \
       "rpm-build" \
       "rpm-devel" \
       "rpm-libs" \
       "groff" \
       "man-pages" \
       "cpio" \
       "go" \
       "cross-i686-tools" \
    )

    RPM_ROOT=$src_root/stage/RPMS
    RPM_LIST=
    for ix in ${!TOOLCHAIN_PKGS[*]}
    do
        RPM=`find $RPM_ROOT -name ${TOOLCHAIN_PKGS[$ix]}-[0-9]*.rpm|awk END{print}`
        RPM_LIST="$RPM_LIST $RPM"
    done

    echo "Installing build toolchain RPMS"

    mkdir -p $chroot_path/var/lib/rpm
    rpm --initdb --dbpath $chroot_path/var/lib/rpm
    rpm -i \
        -v \
        --nodeps \
        --noorder \
        --force \
        --root $chroot_path \
        --define "_dbpath /var/lib/rpm" \
        $RPM_LIST
}

function install_build_rpm()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local rpm=$4
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    echo "Installing RPM: $rpm"

    rpm -i \
        -v \
        --nodeps \
        --noorder \
        --force \
        --root $chroot_path \
        --define "_dbpath /var/lib/rpm" \
        $rpm > /dev/null 2>&1
}

function setup_chroot_base()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    echo "Setting up chroot: $chroot_path"

    mkdir -p $chroot_path
    mkdir -p $chroot_path/dev
    mkdir -p $chroot_path/etc
    mkdir -p $chroot_path/proc
    mkdir -p $chroot_path/run
    mkdir -p $chroot_path/sys
    mkdir -p $chroot_path$TOP_DIR_PATH
    mkdir -p $chroot_path$TOP_DIR_PATH/BUILD
    mkdir -p $chroot_path$TOP_DIR_PATH/SPECS
    mkdir -p $chroot_path$TOP_DIR_PATH/SOURCES
    mkdir -p $chroot_path$TOP_DIR_PATH/RPMS

    (
        cd $src_root/support/package-builder && \
        ./prepare-build-root.sh $chroot_path
    )

    __install_toolchain_rpms $pkg_name $version $src_root

    chroot "$chroot_path" \
        /usr/bin/env -i \
        HOME=/root \
        TERM="$TERM" \
        PS1='\u:\w\$ ' \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
        SHELL=/bin/bash \
        /bin/bash --login +h -c "rpmbuild -ba --clean --nocheck \
           --define \"with_check 0\" \
           --define \"dist .ph2\" \
           --target=i686-photon-linux \
           /sbin/locale-gen.sh"
}

function native_build()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    # Close all fds except stdin, stdout and stderr
    for fd in $(ls /proc/$$/fd/); do
        [ $fd -gt 2 ] && exec {fd}<&-
    done

    echo "Building..."

    chroot "$chroot_path" \
        /usr/bin/env -i \
        HOME=/root \
        TERM="$TERM" \
        PS1='\u:\w\$ ' \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
        SHELL=/bin/bash \
        /bin/bash --login +h -c "rpmbuild -ba --clean --nocheck \
           --define \"with_check 0\" \
           --define \"dist .ph2\" \
           --target=i686-photon-linux \
           /usr/src/photon/SPECS/$pkg_name.spec"
}

function cross_build()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    # Close all fds except stdin, stdout and stderr
    for fd in $(ls /proc/$$/fd/); do
        [ $fd -gt 2 ] && exec {fd}<&-
    done

    echo "Building..."

    chroot "$chroot_path" \
        /usr/bin/env -i \
        HOME=/root \
        TERM="$TERM" \
        PS1='\u:\w\$ ' \
        PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
        SHELL=/bin/bash \
        /bin/bash --login +h -c "rpmbuild -ba --clean --nocheck \
           --define \"with_check 0\" \
           --define \"_host i686-linux-gnu\" \
           --define \"_build x86_64-linux-gnu\" \
           --define \"dist .ph2\" \
           --target=i686-unknown-linux \
           /usr/src/photon/SPECS/$pkg_name.spec"
}

function cross_clean()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    (
        cd $src_root/support/package-builder && \
        ./umount-build-root.sh $chroot_path && \
        ./clean-up-chroot.py $chroot_path
    )
}

function native_clean()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3

    cross_clean $pkg_name $version $src_root
}
