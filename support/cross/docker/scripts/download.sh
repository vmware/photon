#!/bin/bash -xe

function download_binutils() {
    local src_dir=$1
    local version=$2
    local dir_name=binutils-$version
    local file_name=$dir_name.tar.gz

    pushd $src_dir

    if [ ! -f $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://ftp.gnu.org/gnu/binutils/$file_name
    fi

    popd

    return 0
}

function download_kernel() {
    local src_dir=$1
    local version=$2
    local dir_name=linux-$version
    local file_name=$dir_name.tar.xz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://www.kernel.org/pub/linux/kernel/v4.x/$file_name
    fi

    popd

    return 0
}

function download_gcc() {
    local src_dir=$1
    local patch_dir=$2
    local version=$3
    local dir_name=gcc-$version
    local file_name=$dir_name.tar.gz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
	    wget -q --show-progress -nc https://ftp.gnu.org/gnu/gcc/$dir_name/$file_name
    fi

    popd

    return 0
}

function download_glibc() {
    local src_dir=$1
    local version=$2
    local dir_name=glibc-$version
    local file_name=$dir_name.tar.xz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://ftp.gnu.org/gnu/glibc/$file_name
    fi

    popd

    return 0
}

function download_mpfr() {
    local src_dir=$1
    local version=$2
    local dir_name=mpfr-$version
    local file_name=$dir_name.tar.xz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://ftp.gnu.org/gnu/mpfr/$file_name
    fi

    popd

    return 0
}

function download_gmp() {
    local src_dir=$1
    local version=$2
    local dir_name=gmp-$version
    local file_name=$dir_name.tar.xz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://ftp.gnu.org/gnu/gmp/$file_name
    fi

    popd

    return 0
}

function download_mpc() {
    local src_dir=$1
    local version=$2
    local dir_name=mpc-$version
    local file_name=$dir_name.tar.gz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc https://ftp.gnu.org/gnu/mpc/$file_name
    fi

    popd

    return 0
}

function download_isl() {
    local src_dir=$1
    local version=$2
    local dir_name=isl-$version
    local file_name=$dir_name.tar.bz2

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc ftp://gcc.gnu.org/pub/gcc/infrastructure/$file_name
    fi

    popd

    return 0
}

function download_cloog() {
    local src_dir=$1
    local version=$2
    local dir_name=cloog-$version
    local file_name=$dir_name.tar.gz

    pushd $src_dir

    if [ ! -d $file_name ]; then
        echo "Downloading $file_name"
        wget -q --show-progress -nc ftp://gcc.gnu.org/pub/gcc/infrastructure/$file_name
    fi

    popd

    return 0
}

function copy_patches() {
    local src_dir=$1
    local patch_dir=$2
    cp -f $patch_dir/*.patch $src_dir/
}

function showUsage() {
    echo "Usage: download.sh"
    echo "       -b <binutils version>"
    echo "       -c <cloog version>"
    echo "       -i <isl version>"
    echo "       -k <linux kernel version>"
    echo "       -l <glibc version>"
    echo "       -m <mpfr version>"
    echo "       -p <mpc version>"
    echo "       -s <path to SOURCES>"
    echo "       -z <path to patch directory>"
}

#
# Main
#

SRCDIR=
PATCHDIR=
BINUTILS_VERSION=
LINUX_KERNEL_VERSION=
GCC_VERSION=
MPFR_VERSION=
MPC_VERSION=
GMP_VERSION=
ISL_VERSION=
CLOOG_VERSION=

while getopts b:c:g:hi:k:l:m:n:p:s:z: o
do
    case "$o" in
        b)
            BINUTILS_VERSION="$OPTARG"
            ;;
        c)
            CLOOG_VERSION="$OPTARG"
            ;;
        g)
            GCC_VERSION="$OPTARG"
            ;;
        h)
            showUsage
            exit 0
            ;;
        i)
            ISL_VERSION="$OPTARG"
            ;;
        k)
            LINUX_KERNEL_VERSION="$OPTARG"
            ;;
        l)
            GLIBC_VERSION="$OPTARG"
            ;;
        m)
            MPFR_VERSION="$OPTARG"
            ;;
        n)
            GMP_VERSION="$OPTARG"
            ;;
        p)
            MPC_VERSION="$OPTARG"
            ;;
        s)
            SRCDIR="$OPTARG"
            ;;
        z)
            PATCHDIR="$OPTARG"
            ;;
    esac
done

if [ -z "$SRCDIR" ]; then
    echo "Error: No folder for SOURCES specified"
    exit 1
fi

if [ ! -d "$SRCDIR" ]; then
    echo "Error: SOURCES folder does not exist or is not a directory"
    exit 1
fi

if [ -z "$BINUTILS_VERSION" ]; then
    echo "Error; The binutils version was not specified"
    exit 1
fi

if [ -z "$LINUX_KERNEL_VERSION" ]; then
    echo "Error: The linux kernel version was not specified"
    exit 1
fi

if [ -z "$GCC_VERSION" ]; then
    echo "Error: The gcc version was not specified"
    exit 1
fi

if [ -z "$GLIBC_VERSION" ]; then
    echo "Error: The glibc version was not specified"
    exit 1
fi

if [ -z "$MPFR_VERSION" ]; then
    echo "Error: The mpfr version was not specified"
    exit 1
fi

if [ -z "$MPC_VERSION" ]; then
    echo "Error: The mpc version was not specified"
    exit 1
fi

if [ -z "$GMP_VERSION" ]; then
    echo "Error: The gmp version was not specified"
    exit 1
fi

if [ -z "$ISL_VERSION" ]; then
    echo "Error: The ISL version was not specified"
    exit 1
fi

if [ -z "$CLOOG_VERSION" ]; then
    echo "Error: the CLOOG version was not specified"
    exit 1
fi

if [ -z "$PATCHDIR" ]; then
    echo "Error: The patch folder path was not specified"
    exit 1
fi

if [ ! -d "$PATCHDIR" ]; then
    echo "Error: The patch folder path does not exist or is not a directory"
    exit 1
fi

download_binutils $SRCDIR $BINUTILS_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading binutils failed"
    exit $ret
fi

download_kernel $SRCDIR $LINUX_KERNEL_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading linux kernel failed"
    exit $ret
fi

download_gcc $SRCDIR $PATCHDIR $GCC_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading gcc failed"
    exit $ret
fi

download_glibc $SRCDIR $GLIBC_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading glibc failed"
    exit $ret
fi

download_mpfr $SRCDIR $MPFR_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading mpfr failed"
    exit $ret
fi

download_mpc $SRCDIR $MPC_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading mpc failed"
    exit $ret
fi

download_gmp $SRCDIR $GMP_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading gmp failed"
    exit $ret
fi

download_isl $SRCDIR $ISL_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading ISL failed"
    exit $ret
fi

download_cloog $SRCDIR $CLOOG_VERSION
ret=$?
if [ $ret -ne 0 ]; then
    echo "Downloading CLOOG failed"
    exit $ret
fi

copy_patches $SRCDIR $PATCHDIR
ret=$?
if [ $ret -ne 0 ]; then
    echo "Copying patches failed"
    exit $ret
fi

exit 0
