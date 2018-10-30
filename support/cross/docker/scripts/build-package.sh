#!/bin/bash -xe

PROJECT_ROOT=$(pwd)

PKG_NAME=$1
ARCH=$2

function prepare_specs() {
    local pkg_name=$1
    rm -f /usr/src/photon/SPECS/*
    cp -f $PROJECT_ROOT/SPECS/$pkg_name/*.spec /usr/src/photon/SPECS/
}

function prepare_sources() {
    local src_bundle=$1
    if [ ! -f $PROJECT_ROOT/SOURCES/$src_bundle ]; then
        mkdir -p $PROJECT_ROOT/SOURCES && \
        cd $PROJECT_ROOT/SOURCES && \
        wget http://photon-filer.eng.vmware.com/sources/1.0/$src_bundle
    fi
    cp -r $PROJECT_ROOT/SOURCES/$src_bundle /usr/src/photon/SOURCES/
}

function prepare_patches() {
    local pkg_name=$1
    cp -f $PROJECT_ROOT/SPECS/$pkg_name/*.patch /usr/src/photon/SOURCES/
}

function prepare_sources_from_specs() {
    local pkg_name=$1
    local src_bundle=$2
    if [ ! -f $PROJECT_ROOT/SOURCES/$src_bundle ]; then
        mkdir -p $PROJECT_ROOT/SOURCES && \
        cp -r $PROJECT_ROOT/SPECS/$pkg_name/$src_bundle $PROJECT_ROOT/SOURCES/
    fi
    cp -r $PROJECT_ROOT/SOURCES/$src_bundle /usr/src/photon/SOURCES/
}

function prepare_sources_from_specs_path() {
    local pkg_name=$1
    local path=$2
    local src_bundle=$3
    if [ ! -f $PROJECT_ROOT/SOURCES/$src_bundle ]; then
        mkdir -p $PROJECT_ROOT/SOURCES && \
        cp -r $PROJECT_ROOT/SPECS/$pkg_name/$path/$src_bundle $PROJECT_ROOT/SOURCES/
    fi
    cp -r $PROJECT_ROOT/SOURCES/$src_bundle /usr/src/photon/SOURCES/
}

function build_acl_i686() {
    prepare_specs acl

    prepare_sources acl-2.2.53.tar.gz

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/attr-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/attr-devel-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/attr*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/acl.spec
}

function build_attr_i686() {
    prepare_specs attr

    prepare_sources attr-2.4.48.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/attr.spec
}

function build_bash_i686() {
    prepare_specs bash

    prepare_patches bash
    prepare_sources_from_specs bash bash44-001
    prepare_sources_from_specs bash bash44-002
    prepare_sources_from_specs bash bash44-003
    prepare_sources_from_specs bash bash44-004
    prepare_sources_from_specs bash bash44-005
    prepare_sources_from_specs bash bash44-006
    prepare_sources_from_specs bash bash44-007
    prepare_sources_from_specs bash bash44-008
    prepare_sources_from_specs bash bash44-009
    prepare_sources_from_specs bash bash44-010
    prepare_sources_from_specs bash bash44-011
    prepare_sources_from_specs bash bash44-012
    prepare_sources_from_specs bash bash_completion

    prepare_sources bash-4.4.tar.gz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses-libs-*.rpm \
        $PROJECT_ROOT/RPMS/i686/readline-*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/bash.spec
}

function build_bzip2_i686() {
    prepare_specs bzip2

    prepare_sources bzip2-1.0.6.tar.gz

    prepare_patches bzip2

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/bzip2.spec
}

function build_ca_certificates_i686() {
    prepare_specs ca-certificates

    prepare_sources_from_specs ca-certificates certdata.txt

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/openssl-[0-9].*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/ca-certificates.spec
}

function build_coreutils_i686() {
    prepare_specs coreutils

    prepare_patches coreutils
    prepare_sources_from_specs coreutils serial-console.sh

    prepare_sources coreutils-8.30.tar.xz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/gmp-*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/coreutils.spec
}

function build_cracklib_i686() {
    prepare_specs cracklib

    prepare_sources cracklib-2.9.6.tar.gz
    prepare_sources cracklib-words-2.9.6.gz

    prepare_patches cracklib

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/gzip-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-dicts-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/cracklib.spec
}
function build_diffutils_i686() {
    prepare_specs diffutils

    prepare_sources diffutils-3.6.tar.xz

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/coreutils-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/coreutils*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/diffutils.spec
}

function build_e2fsprogs_i686() {
    prepare_specs e2fsprogs

    prepare_sources e2fsprogs-1.44.3.tar.gz

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-devel-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/util-linux*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/e2fsprogs.spec
}

function build_ed_i686() {
    prepare_specs ed

    prepare_sources ed-1.14.2.tar.gz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/ed.spec
}

function build_elfutils_i686() {
    prepare_specs elfutils

    prepare_sources elfutils-0.174.tar.bz2

    prepare_patches elfutils

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/elfutils-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/elfutils-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/elfutils-libelf-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/elfutils-libelf-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/zlib-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/zlib-devel-[0-9].*.rpm

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/bzip2*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/elfutils.spec
}

function build_expat_i686() {
    prepare_specs expat

    prepare_sources expat-2.2.6.tar.bz2

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/expat.spec
}

function build_file_i686() {
    prepare_specs file

    prepare_sources file-5.34.tar.gz

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/file-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/file-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "sysroot /target" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/file.spec
}

function build_filesystem_i686() {
    prepare_specs filesystem

    prepare_sources filesystem-1.1.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/filesystem.spec
}

function build_findutils_i686() {
    prepare_specs findutils

    prepare_sources findutils-4.6.0.tar.gz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/findutils.spec
}

function build_glib_i686() {
    prepare_specs glib

    prepare_sources glib-2.58.0.tar.xz

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/pcre-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/pcre-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/pcre-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libffi-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libffi-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/pkg-config-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cmake-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/which-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/gettext-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/expat-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/expat-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/python2-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/python2-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/python-xml-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/pcre*.rpm \
        $PROJECT_ROOT/RPMS/i686/libffi*.rpm \
        $PROJECT_ROOT/RPMS/i686/util-linux*.rpm \
        $PROJECT_ROOT/RPMS/i686/elfutils*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/glib.spec
}

function build_glibc_i686() {
    prepare_specs glibc

    prepare_sources glibc-2.28.tar.xz
    prepare_sources_from_specs glibc locale-gen.sh
    prepare_sources_from_specs glibc locale-gen.conf
    prepare_sources_from_specs glibc glibc-2.25-fhs-1.patch
    prepare_sources_from_specs glibc glibc-2.24-bindrsvport-blacklist.patch
    prepare_sources_from_specs glibc 0002-malloc-arena-fix.patch

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/glibc.spec
}

function build_gmp_i686() {
    prepare_specs gmp

    prepare_sources gmp-6.1.2.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gmp.spec
}

function build_ncurses_i686() {
    prepare_specs ncurses

    prepare_sources ncurses-6.1-20180908.tgz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/ncurses.spec
}

function build_net_tools_i686() {
    prepare_specs net-tools

    prepare_sources net-tools-1.60.tar.bz2

    prepare_patches net-tools

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/nspr-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/net-tools.spec
}

function build_nspr_i686() {
    prepare_specs nspr

    prepare_sources nspr-4.20.tar.gz

    prepare_patches nspr

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/nspr-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "dist .ph2" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/nspr.spec
}

function build_gawk_i686() {
    prepare_specs gawk

    prepare_sources gawk-4.2.1.tar.xz

    # Install host RPMs
    rpm -Uvh --force --nodeps \
             $PROJECT_ROOT/stage/RPMS/x86_64/readline-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gawk.spec
}

function build_gdbm_i686() {
    prepare_specs gdbm

    prepare_sources gdbm-1.18.tar.gz

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gdbm.spec
}

function build_gettext_i686() {
    prepare_specs gettext

    prepare_sources gettext-0.19.8.1.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gettext.spec
}

function build_gperf_i686() {
    prepare_specs gperf

    prepare_sources gperf-3.1.tar.gz

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gperf.spec
}

function build_grep_i686() {
    prepare_specs grep

    prepare_sources grep-3.1.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/grep.spec
}

function build_groff_i686() {
    prepare_specs groff

    prepare_sources groff-1.22.3.tar.gz

    # Install host RPMs
    rpm -Uvh --force --nodeps \
             $PROJECT_ROOT/stage/RPMS/x86_64/groff-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/perl-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/perl-DBD-SQLite-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/perl-DBI-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/noarch/perl-DBIx-Simple-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/noarch/perl-File-HomeDir-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/noarch/perl-File-Which-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/noarch/perl-Object-Accessor-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/gdbm-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/groff.spec
}

function build_gzip_i686() {
    prepare_specs gzip

    prepare_sources gzip-1.9.tar.xz

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/gzip.spec
}

function build_iana_etc_i686() {
    prepare_specs iana-etc

    prepare_sources iana-etc-2.30.tar.bz2

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/iana-etc.spec
}

function build_iproute2_i686() {
    prepare_specs iproute2

    prepare_sources iproute2-4.18.0.tar.xz

    prepare_patches iproute2

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/elfutils*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/iproute2.spec
}

function build_iputils_i686() {
    prepare_specs iputils

    prepare_sources iputils-s20180629.tar.gz

    rpm -Uvh --force \
             $PROJECT_ROOT/stage/RPMS/x86_64/libcap-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libcap-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgcrypt-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgcrypt-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgpg-error-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgpg-error-devel-[0-9].*.rpm

    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/libcap*.rpm \
        $PROJECT_ROOT/RPMS/i686/libgpg-error*.rpm \
        $PROJECT_ROOT/RPMS/i686/libgcrypt*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/iputils.spec
}

function build_kbd_i686() {
    prepare_specs kbd

    prepare_sources kbd-2.0.4.tar.xz

    prepare_patches kbd

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/check-[0-9].*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/kbd.spec
}

function build_kmod_i686() {
    prepare_specs kmod

    prepare_sources kmod-25.tar.xz
    prepare_patches kmod

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/xz-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/xz-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/xz-devel-[0-9].*.rpm
    # Install target RPMs
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/xz*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm \

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/kmod.spec
}

function build_less_i686() {
    prepare_specs less

    prepare_sources less-530.tar.gz

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-terminfo-[0-9].*.rpm
    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses-*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --define "sysroot /target" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/less.spec
}

function build_libarchive_i686() {
    prepare_specs libarchive

    prepare_sources libarchive-3.3.3.tar.gz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/xz*.rpm

    rpm -qa | grep xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --define "sysroot /target" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libarchive.spec
}

function build_libcap_i686() {
    prepare_specs libcap

    prepare_sources libcap-2.25.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libcap.spec
}

function build_libdb_i686() {
    prepare_specs libdb

    prepare_sources db-5.3.28.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libdb.spec
}

function build_libdnet_i686() {
    prepare_specs libdnet

    prepare_sources libdnet-1.11.tar.gz

    prepare_patches libdnet

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libdnet.spec
}

function build_libffi_i686() {
    prepare_specs libffi

    prepare_sources libffi-3.2.1.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libffi.spec
}

function build_libgcrypt_i686() {
    prepare_specs libgcrypt

    prepare_sources libgcrypt-1.8.3.tar.bz2

    prepare_patches libgcrypt

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/libgpg-error-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgpg-error-devel-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/libgpg-error*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libgcrypt.spec
}

function build_libgpg_error_i686() {
    prepare_specs libgpg-error

    prepare_sources libgpg-error-1.32.tar.bz2

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libgpg-error.spec
}

function build_libmspack_i686() {
    prepare_specs libmspack

    prepare_sources libmspack-0.7.1alpha.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libmspack.spec
}

function build_libpipeline_i686() {
    prepare_specs libpipeline

    prepare_sources libpipeline-1.5.0.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libpipeline.spec
}

function build_libssh2_i686() {
    prepare_specs libssh2

    prepare_sources libssh2-1.8.0.tar.gz

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/openssl-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/openssl-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/zlib-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/openssl*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/libssh2.spec
}

function build_linux_pam_i686() {
    prepare_specs Linux-PAM

    prepare_sources Linux-PAM-1.3.0.tar.bz2

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-dicts-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/cracklib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/Linux-PAM.spec
}

function build_man_db_i686() {
    prepare_specs man-db

    prepare_sources man-db-2.7.6.tar.xz

    rpm -Uvh --nodeps \
            $PROJECT_ROOT/stage/RPMS/x86_64/libpipeline-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/libpipeline-devel-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/gdbm-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/gdbm-devel-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/xz-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/xz-libs-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/groff-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/perl-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/perl-DBD-SQLite-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/perl-DBI-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/noarch/perl-DBIx-Simple-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/noarch/perl-File-HomeDir-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/noarch/perl-File-Which-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/noarch/perl-Object-Accessor-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
            $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/libpipeline*.rpm \
        $PROJECT_ROOT/RPMS/i686/xz*.rpm \
        $PROJECT_ROOT/RPMS/i686/gdbm*.rpm \
        $PROJECT_ROOT/RPMS/i686/groff*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/man-db.spec
}

function build_openssl_release_i686() {
    prepare_specs openssl

    prepare_sources openssl-1.0.2p.tar.gz
    prepare_sources_from_specs openssl rehash_ca_certificates.sh

    prepare_patches openssl

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/e2fsprogs-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/util-linux-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/openssl-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/util-linux*.rpm \
        $PROJECT_ROOT/RPMS/i686/expat*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --define "_arch i686" \
       --define "photon_release_version 3.0" \
       --define "photon_build_number 20" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/openssl.spec
}

function build_pcre_i686() {
    prepare_specs pcre

    prepare_sources pcre-8.42.tar.bz2

    # Install/Update host RPMs
    rpm -Uvh --force --nodeps \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/bzip2-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/readline-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/readline-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgcc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgcc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libgcc-atomic-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libstdc++-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/libstdc++-devel-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/bzip2*.rpm \
        $PROJECT_ROOT/RPMS/i686/zlib*.rpm \
        $PROJECT_ROOT/RPMS/i686/readline*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/pcre.spec
}

function build_photon_release_i686() {
    prepare_specs photon-release

    prepare_sources photon-release-2.0.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --define "_arch i686" \
       --define "photon_release_version 3.0" \
       --define "photon_build_number 20" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/photon-release.spec
}

function build_photon_repos_i686() {
    prepare_specs photon-repos

    prepare_sources photon-repos-2.0.tar.gz
    prepare_sources_from_specs photon-repos VMWARE-RPM-GPG-KEY
    prepare_sources_from_specs photon-repos photon-iso.repo
    prepare_sources_from_specs photon-repos photon.repo
    prepare_sources_from_specs photon-repos photon-debuginfo.repo
    prepare_sources_from_specs photon-repos photon-repos.spec
    prepare_sources_from_specs photon-repos photon-extras.repo
    prepare_sources_from_specs photon-repos photon-updates.repo

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/photon-repos.spec
}

function build_popt_i686() {
    prepare_specs popt

    prepare_sources popt-1.16.tar.gz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/popt.spec
}

function build_psmisc_i686() {
    prepare_specs psmisc

    prepare_sources psmisc-23.2.tar.xz

    # Install/Update host RPMs
    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-libs-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/ncurses-terminfo-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/psmisc.spec
}

function build_procps_ng_i686() {
    prepare_specs procps-ng

    prepare_sources procps-ng-3.3.15.tar.xz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/procps-ng.spec
}

function build_readline_i686() {
    prepare_specs readline

    prepare_sources readline-7.0.tar.gz

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/ncurses*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/readline.spec
}

function build_shadow_i686() {
    prepare_specs shadow

    prepare_sources shadow-4.6.tar.xz
    prepare_patches shadow
    prepare_sources_from_specs_path shadow pam.d chage
    prepare_sources_from_specs_path shadow pam.d chpasswd
    prepare_sources_from_specs_path shadow pam.d login
    prepare_sources_from_specs_path shadow pam.d other
    prepare_sources_from_specs_path shadow pam.d passwd
    prepare_sources_from_specs_path shadow pam.d sshd
    prepare_sources_from_specs_path shadow pam.d su
    prepare_sources_from_specs_path shadow pam.d system-account
    prepare_sources_from_specs_path shadow pam.d system-auth
    prepare_sources_from_specs_path shadow pam.d system-password
    prepare_sources_from_specs_path shadow pam.d system-session

    rpm -Uvh $PROJECT_ROOT/stage/RPMS/x86_64/gzip-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-dicts-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/cracklib-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/Linux-PAM-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/Linux-PAM-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-devel-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-i18n-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-lang-[0-9].*.rpm \
             $PROJECT_ROOT/stage/RPMS/x86_64/glibc-iconv-[0-9].*.rpm

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/cracklib*.rpm \
        $PROJECT_ROOT/RPMS/i686/Linux-PAM*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/shadow.spec
}

function build_sqlite_i686() {
    prepare_specs sqlite

    prepare_sources sqlite-2.8.17.tar.gz
    prepare_sources sqlite-autoconf-3220000.tar.gz
    prepare_patches sqlite

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/sqlite.spec
}

function build_tar_i686() {
    prepare_specs tar

    prepare_sources tar-1.30.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/tar.spec
}

function build_unzip_i686() {
    prepare_specs unzip

    prepare_sources unzip60.tar.gz

    prepare_patches unzip

    mkdir -p /target/var/lib/rpm && \
    rpm --initdb --dbpath /target/var/lib/rpm && \
    rpm --root /target \
        --define "_dbpath /var/lib/rpm" \
        -i \
        --force \
        --nodeps \
        $PROJECT_ROOT/RPMS/i686/filesystem*.rpm \
        $PROJECT_ROOT/RPMS/i686/glibc*.rpm \
        $PROJECT_ROOT/RPMS/i686/bzip2*.rpm

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/unzip.spec
}

function build_util_linux_i686() {
    prepare_specs util-linux

    prepare_sources util-linux-2.32.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/util-linux.spec
}

function build_xz_i686() {
    prepare_specs xz

    prepare_sources xz-5.2.4.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/xz.spec
}

function build_zlib_i686() {
    prepare_specs zlib

    prepare_sources zlib-1.2.11.tar.xz

    rpmbuild -ba --clean --nocheck \
       --define "with_check 0" \
       --define "_host i686-linux-gnu" \
       --define "_build x86_64-linux-gnu" \
       --define "dist .ph2" \
       --target=i686-unknown-linux \
       /usr/src/photon/SPECS/zlib.spec
}

case $ARCH in
    i686)
        mkdir -p $PROJECT_ROOT/RPMS/i686
        ;;
    *)
        echo "Error: Unsupported architecture - $ARCH"
        exit 1
        ;;
esac

mkdir -p /usr/src/photon/BUILD && rm -rf /usr/src/photon/BUILD/*
mkdir -p /usr/src/photon/BUILDROOT && rm -rf /usr/src/photon/BUILDROOT/*
mkdir -p /usr/src/photon/RPMS
mkdir -p /usr/src/photon/tmp && rm -rf /usr/src/photon/tmp/*
mkdir -p /usr/src/photon/SOURCES
mkdir -p /usr/src/photon/SPECS && rm -rf /usr/src/photon/SPECS/*

case $PKG_NAME in
    acl)
        build_acl_$ARCH
        ;; 
    attr)
        build_attr_$ARCH
        ;; 
    bash)
        build_bash_$ARCH
        ;; 
    bzip2)
        build_bzip2_$ARCH
        ;; 
    ca-certificates)
        build_ca_certificates_$ARCH
        ;; 
    coreutils)
        build_coreutils_$ARCH
        ;; 
    cracklib)
        build_cracklib_$ARCH
        ;; 
    diffutils)
        build_diffutils_$ARCH
        ;; 
    ed)
        build_ed_$ARCH
        ;; 
    e2fsprogs)
        build_e2fsprogs_$ARCH
        ;; 
    elfutils)
        build_elfutils_$ARCH
        ;; 
    expat)
        build_expat_$ARCH
        ;; 
    file)
        build_file_$ARCH
        ;;
    filesystem)
        build_filesystem_$ARCH
        ;;
    findutils)
        build_findutils_$ARCH
        ;; 
    gawk)
        build_gawk_$ARCH
        ;;
    gdbm)
        build_gdbm_$ARCH
        ;;
    gettext)
        build_gettext_$ARCH
        ;;
    glib)
        build_glib_$ARCH
        ;;
    glibc)
        build_glibc_$ARCH
        ;;
    gmp)
        build_gmp_$ARCH
        ;;
    gperf)
        build_gperf_$ARCH
        ;;
    grep)
        build_grep_$ARCH
        ;;
    groff)
        build_groff_$ARCH
        ;;
    gzip)
        build_gzip_$ARCH
        ;;
    iana-etc)
        build_iana_etc_$ARCH
        ;;
    iproute2)
        build_iproute2_$ARCH
        ;;
    iputils)
        build_iputils_$ARCH
        ;;
    kbd)
        build_kbd_$ARCH
        ;;
    kmod)
        build_kmod_$ARCH
        ;;
    less)
        build_less_$ARCH
        ;;
    libarchive)
        build_libarchive_$ARCH
        ;;
    libcap)
        build_libcap_$ARCH
        ;;
    libdb)
        build_libdb_$ARCH
        ;;
    libdnet)
        build_libdnet_$ARCH
        ;;
    libffi)
        build_libffi_$ARCH
        ;;
    libgcrypt)
        build_libgcrypt_$ARCH
        ;;
    libgpg-error)
        build_libgpg_error_$ARCH
        ;;
    libmspack)
        build_libmspack_$ARCH
        ;;
    libpipeline)
        build_libpipeline_$ARCH
        ;;
    libssh2)
        build_libssh2_$ARCH
        ;;
    linux-pam)
        build_linux_pam_$ARCH
        ;;
    man-db)
        build_man_db_$ARCH
        ;;
    net-tools)
        build_net_tools_$ARCH
        ;;
    ncurses)
        build_ncurses_$ARCH
        ;;
    nspr)
        build_nspr_$ARCH
        ;;
    openssl)
        build_openssl_release_$ARCH
        ;;
    pcre)
        build_pcre_$ARCH
        ;;
    photon-release)
        build_photon_release_$ARCH
        ;;
    photon-repos)
        build_photon_repos_$ARCH
        ;;
    popt)
        build_popt_$ARCH
        ;;
    procps-ng)
        build_procps_ng_$ARCH
        ;;
    psmisc)
        build_psmisc_$ARCH
        ;;
    readline)
        build_readline_$ARCH
        ;;
    shadow)
        build_shadow_$ARCH
        ;;
    sqlite)
        build_sqlite_$ARCH
        ;;
    tar)
        build_tar_$ARCH
        ;;
    unzip)
        build_unzip_$ARCH
        ;;
    util-linux)
        build_util_linux_$ARCH
        ;;
    xz)
        build_xz_$ARCH
        ;;
    zlib)
        build_zlib_$ARCH
        ;;
    *)
        echo "Error. Unrecognized package - $PKG_NAME"
        ;;
esac

cp -r /usr/src/photon/RPMS/* $PROJECT_ROOT/RPMS/
