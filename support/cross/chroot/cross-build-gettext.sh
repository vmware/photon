#!/bin/bash

. ./cross-build-defines.sh

pkg_name=gettext
version=0.19.8.1

function setup_chroot()
{
    local pkg_name=$1
    local version=$2
    local src_root=$3
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    setup_chroot_base $pkg_name $version $src_root

    cp -f $src_root/SOURCES/$pkg_name-$version*.tar.xz \
          $chroot_path$TOP_DIR_PATH/SOURCES/
    cp -f $src_root/SPECS/$pkg_name/*.spec $chroot_path$TOP_DIR_PATH/SPECS/
}

function build()
{
    local src_root=$(cd ../../..;pwd)
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    setup_chroot $pkg_name $version $src_root
    cross_build $pkg_name $version $src_root
    cp -r $chroot_path$TOP_DIR_PATH/RPMS/* $src_root/stage/RPMS/
    cp -r $chroot_path$TOP_DIR_PATH/SRPMS/* $src_root/stage/SRPMS/
}

function clean()
{
    local src_root=$(cd ../../..;pwd)
    local chroot_path=$(get_chroot_path $pkg_name $version $src_root)

    cross_clean $pkg_name $version $src_root
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

