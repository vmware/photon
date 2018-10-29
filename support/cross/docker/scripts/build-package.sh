#!/bin/bash -xe

PROJECT_ROOT=$(pwd)

PKG_NAME=$1
ARCH=$2

function prepare_specs() {
    local pkg_name=$1
    rm -f /usr/src/photon/SPECS/*
    cp -f $PROJECT_ROOT/SPECS/$pkg_name/* /usr/src/photon/SPECS/
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
    diffutils)
        build_diffutils_$ARCH
        ;; 
    ed)
        build_ed_$ARCH
        ;; 
    e2fsprogs)
        build_e2fsprogs_$ARCH
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
    gettext)
        build_gettext_$ARCH
        ;;
    glibc)
        build_glibc_$ARCH
        ;;
    gmp)
        build_gmp_$ARCH
        ;;
    grep)
        build_grep_$ARCH
        ;;
    groff)
        build_groff_$ARCH
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
    libgpg-error)
        build_libgpg_error_$ARCH
        ;;
    libmspack)
        build_libmspack_$ARCH
        ;;
    libssh2)
        build_libssh2_$ARCH
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
    photon-release)
        build_photon_release_$ARCH
        ;;
    photon-repos)
        build_photon_repos_$ARCH
        ;;
    popt)
        build_popt_$ARCH
        ;;
    readline)
        build_readline_$ARCH
        ;;
    sqlite)
        build_sqlite_$ARCH
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
