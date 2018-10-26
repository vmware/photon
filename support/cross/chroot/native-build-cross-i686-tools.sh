#!/bin/bash

. ./cross-build-defines.sh

pkg_name=cross-i686-tools
version=1.0.0

function setup_chroot()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)
    local sources=( \
            binutils-2.28.tar.gz \
            linux-4.18.11.tar.xz \
            gcc-6.3.0.tar.gz \
            glibc-2.26.tar.xz \
            mpfr-3.1.5.tar.xz \
            gmp-6.1.2.tar.xz \
            mpc-1.0.3.tar.gz \
            isl-0.14.tar.bz2 \
            cloog-0.18.1.tar.gz \
          )
    local patches=( \
            gcc-patch-fix-glibc-struct_ucontext_t.patch \
            gcc-patch-include-sys-param.patch \
            gcc-patch-sanitizer-pr-81066.patch \
            ubsan_use_new_style.patch \
          )
    local buildreqs=( \
            unzip-6.0-10.ph3.x86_64.rpm \
            wget-1.19.5-1.ph3.x86_64.rpm \
          )

    setup_chroot_base $pkg_name $version $src_root

    for r in ${!buildreqs[*]}
    do
        install_build_rpm \
           $pkg_name \
           $version \
           $src_root \
           $src_root/stage/RPMS/x86_64/${buildreqs[$r]}
    done

    cp -f $src_root/SPECS/cross-tools/$pkg_name.spec \
          $chroot_path$TOP_DIR_PATH/SPECS/

    for s in ${!sources[*]}
    do
        cp -f $src_root/SOURCES/${sources[$s]} \
              $chroot_path$TOP_DIR_PATH/SOURCES/
    done

    for p in ${!patches[*]}
    do
        cp -f $src_root/SPECS/cross-tools/${patches[$p]} \
              $chroot_path$TOP_DIR_PATH/SOURCES/
    done
}

function build()
{
    local src_root=$(cd ../../..;pwd)

    setup_chroot $pkg_name $version $src_root
    native_build $pkg_name $version $src_root
    cp -r $chroot_path$TOP_DIR_PATH/RPMS/* $src_root/stage/RPMS/
    cp -r $chroot_path$TOP_DIR_PATH/SRPMS/* $src_root/stage/SRPMS/
}

function clean()
{
    local src_root=$(cd ../../..;pwd)
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    native_clean $pkg_name $version $src_root
    rm -rf $chroot_path
}

function help() # Show a list of functions
{
    grep "^function" $0
}

if [ "_$1" = "_" ]; then
    help
else
    "$@"
fi

