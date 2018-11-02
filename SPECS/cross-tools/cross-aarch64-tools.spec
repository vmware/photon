%define binutils_version 2.28
%define linux_kernel_version 4.18.9
%define gcc_version 7.3.0
%define glibc_version 2.28
%define mpfr_version 3.1.5
%define gmp_version 6.1.2
%define mpc_version 1.0.3
%define isl_version 0.16.1
%define cloog_version 0.18.1

Name:    cross-aarch64-tools
Summary: VMware Photon Cross Compiler for AARCH64
Version: 1.0.0
Release: 3%{?_dist}
Group:   Compiler
Vendor:  VMware, Inc.
Distribution: Photon
License: Apache 2
URL:     http://github.com/vmware/photon
Source0: https://ftp.gnu.org/gnu/binutils/binutils-%{binutils_version}.tar.gz
Source1: https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{linux_kernel_version}.tar.xz
Source2: https://ftp.gnu.org/gnu/gcc/gcc-%{gcc_version}/gcc-%{gcc_version}.tar.gz
Source3: https://ftp.gnu.org/gnu/glibc/glibc-%{glibc_version}.tar.xz
Source4: https://ftp.gnu.org/gnu/mpfr/mpfr-%{mpfr_version}.tar.xz
Source5: https://ftp.gnu.org/gnu/gmp/gmp-%{gmp_version}.tar.xz
Source6: https://ftp.gnu.org/gnu/mpc/mpc-%{mpc_version}.tar.gz
Source7: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source8: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz
Patch0:   libsanitizer-avoidustat.h-glibc-2.28.patch
Patch1:   PLUGIN_TYPE_CAST.patch
BuildArch: x86_64
Provides: libgcc_s.so.1
Provides: libgcc_s.so.1(GCC_3.0)
Provides: libgcc_s.so.1(GCC_3.3)
Provides: libgcc_s.so.1(GCC_4.2.0)
Provides: libgcc_s.so.1(GLIBC_2.0)
BuildRequires: binutils >= 2.31
BuildRequires: bison >= 3.0.4
BuildRequires: bzip2 >= 1.0.6
BuildRequires: diffutils >= 3.5
BuildRequires: file >= 5.30
BuildRequires: findutils >= 4.6.0
BuildRequires: gawk >= 4.1.4
BuildRequires: gcc >= 6.3.0
BuildRequires: glibc-devel >= 2.26
BuildRequires: gzip >= 1.8
BuildRequires: linux-api-headers >= 4.9.124
BuildRequires: make >= 4.2.1
BuildRequires: patch >= 2.7.5
BuildRequires: rpm >= 4.13.0.1
BuildRequires: rpm-build >= 4.13.0.1
BuildRequires: rpm-devel >= 4.13.0.1
BuildRequires: sed >= 4.4
BuildRequires: tar >= 1.29
BuildRequires: texinfo >= 6.3
BuildRequires: unzip >= 6.0
BuildRequires: wget >= 1.19.1
BuildRequires: xz >= 5.2.3
Requires: autoconf >= 2.69
Requires: automake >= 1.15
Requires: libtool >= 2.4.6
Requires: binutils >= 2.31
Requires: bison >= 3.0.4
Requires: bzip2 >= 1.0.6
Requires: cpio >= 2.12
Requires: diffutils >= 3.5
Requires: elfutils-libelf-devel >= 0.169
Requires: elfutils >= 0.169
Requires: elfutils-devel >= 0.169
Requires: file >= 5.30
Requires: findutils >= 4.6.0
Requires: gawk >= 4.1.4
Requires: gcc >= 6.3.0
Requires: gettext >= 0.19.8
Requires: glibc-devel >= 2.26
Requires: glibc-iconv >= 2.26
Requires: glibc-i18n >= 2.26
Requires: glibc-lang >= 2.26
Requires: gzip >= 1.8
Requires: libgcc >= 6.3.0
Requires: linux-api-headers >= 4.9.124
Requires: make >= 4.2.1
Requires: ncurses >= 6.0
Requires: ncurses-devel >= 6.0
Requires: ncurses-terminfo >= 6.0
Requires: patch >= 2.7.5
Requires: rpm >= 4.13.0.1
Requires: rpm-build >= 4.13.0.1
Requires: rpm-devel >= 4.13.0.1
Requires: sed >= 4.4
Requires: tar >= 1.29
Requires: texinfo >= 6.3
Requires: unzip >= 6.0
Requires: wget >= 1.19.1
Requires: xz >= 5.2.3
Requires: xz-devel >= 5.2.3

%define cross_prefix /opt/cross
%define target_arch aarch64-linux-gnu
%define target_linux_arch arm64
%define sysroot /target
%define _bindir %{cross_prefix}/bin
%define _archdir %{cross_prefix}/%{target_arch}
%define _includedir %{cross_prefix}/include
%define _libdir %{cross_prefix}/lib
%define _lib64dir %{cross_prefix}/lib64
%define _libexecdir %{cross_prefix}/libexec
%define _sharedir %{cross_prefix}/share

%description
Photon Cross Compiler for ARM64

%prep

%setup -c -q
%setup -T -D -q -a 1
%setup -T -D -q -a 2
%setup -T -D -q -a 3
%setup -T -D -q -a 4
%setup -T -D -q -a 5
%setup -T -D -q -a 6
%setup -T -D -q -a 7
%setup -T -D -q -a 8

cd gcc-%{gcc_version}
%patch0 -p1
%patch1 -p1
ln -sf `ls -1d ../mpfr-*/` mpfr
ln -sf `ls -1d ../gmp-*/` gmp
ln -sf `ls -1d ../mpc-*/` mpc
ln -sf `ls -1d ../isl-*/` isl
ln -sf `ls -1d ../cloog-*/` cloog

%build

builddir=$RPM_BUILD_DIR/%{name}-%{version}

echo "Building binutils for arch - %{target_arch}"

mkdir -p $builddir/build-binutils-%{target_arch} && \
cd $builddir/build-binutils-%{target_arch} && \
$builddir/binutils-%{binutils_version}/configure \
    --prefix=%{cross_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --disable-multilib && \
make configure-host && \
make && \
make install

###
### Step 2
###

echo "Building Linux Headers for arch - %{target_arch}"

cd $builddir/linux-%{linux_kernel_version} && \
make mrproper && \
make ARCH=%{target_linux_arch} headers_check && \
make ARCH=%{target_linux_arch} \
     INSTALL_HDR_PATH=%{cross_prefix}/%{target_arch} \
     headers_install
mkdir -p %{sysroot}/usr/include
cp -rv %{cross_prefix}/%{target_arch}/include/* %{sysroot}/usr/include
find %{sysroot}/usr/include -name .install -or -name ..install.cmd | \
     xargs rm -fv

###
### Step 3
###

echo "Building GCC Stage 1 for %{target_arch}: C and C++ Cross Compilers"

mkdir -p $builddir/build-gcc-%{target_arch} && \
cd $builddir/build-gcc-%{target_arch} && \
$builddir/gcc-%{gcc_version}/configure \
    --prefix=%{cross_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --enable-plugins \
    --enable-languages=c \
    --enable-threads=posix \
    --enable-linker-build-id \
    --disable-multilib && \
make %{?_smp_mflags} all-gcc && \
make install-gcc

###
### Step 4
###

echo "Building GLIBC Stage 1 for %{target_arch}: Standard C Library Headers"

export PATH=%{cross_prefix}/bin:$PATH

mkdir -p $builddir/build-glibc-%{target_arch} && \
cd $builddir/build-glibc-%{target_arch} && \
$builddir/glibc-%{glibc_version}/configure \
    --prefix=/usr \
    --libexecdir=/usr/lib/glibc \
    --build=$MACHTYPE \
    --host=%{target_arch} \
    --target=%{target_arch} \
    --with-headers=%{sysroot}/usr/include \
    --disable-multilib \
    libc_cv_forced_unwind=yes && \
make install-bootstrap-headers=yes install-headers install_root=%{sysroot} && \
make %{?_smp_mflags} csu/subdir_lib && \
mkdir -p %{sysroot}/usr/lib && \
install csu/crt1.o csu/crti.o csu/crtn.o \
            %{sysroot}/usr/lib && \
%{target_arch}-gcc \
    -nostdlib \
    -nostartfiles \
    -shared \
    -x c /dev/null \
    -o %{sysroot}/usr/lib/libc.so && \
mkdir -p %{sysroot}/usr/include/gnu && \
touch %{sysroot}/usr/include/gnu/stubs.h

###
### Step 5
###

echo "Building GCC Stage 2 for %{target_arch}: Compiler support library"

cd $builddir/build-gcc-%{target_arch} && \
$builddir/gcc-%{gcc_version}/configure \
    --prefix=%{cross_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --enable-shared \
    --enable-languages=c,c++ \
    --enable-threads=posix \
    --enable-linker-build-id \
    --enable-__cxa_atexit \
    --disable-multilib && \
make %{?_smp_mflags} all-target-libgcc && \
make install-target-libgcc

###
### Step 6
###

echo "Building GLIBC Stage 2 for %{target_arch}: Standard C Library"

cd $builddir/build-glibc-%{target_arch} && \
make %{?_smp_mflags} && \
make install install_root=%{sysroot}

###
### Step 7
###

echo "Building GCC Stage 3 for %{target_arch}: Standard C++ Library"

cd $builddir/build-gcc-%{target_arch} && \
make %{?_smp_mflags} all && \
make install

mv %{sysroot}/lib/* %{sysroot}/usr/lib/
mv %{sysroot}/sbin/* %{sysroot}/usr/sbin/
rm -rf %{sysroot}/lib && ln -s %{sysroot}/usr/lib %{sysroot}/lib
rm -rf %{sysroot}/sbin && ln -s %{sysroot}/usr/sbin %{sysroot}/sbin

%install

mkdir -p %{buildroot}%{sysroot}
cp -av %{sysroot}/* %{buildroot}/%{sysroot}/

CROSS_TOOLCHAIN_PKG_CONFIG=%{buildroot}%{_bindir}/%{target_arch}-pkg-config

cat > $CROSS_TOOLCHAIN_PKG_CONFIG << EOF
#!/bin/sh

SYSROOT=%{sysroot}

export PKG_CONFIG_DIR=
export PKG_CONFIG_LIBDIR=\${SYSROOT}/usr/lib/pkgconfig:\${SYSROOT}/usr/share/pkgco
nfig
export PKG_CONFIG_SYSROOT_DIR=\${SYSROOT}

exec pkg-config "$@"
EOF
chmod +x $CROSS_TOOLCHAIN_PKG_CONFIG

%files

%defattr(-,root,root)

%{_bindir}/*
%{_archdir}/*
%{_libdir}/*
%{_lib64dir}/*
%{_libexecdir}/*
%{_sharedir}/*
%{sysroot}/*

%changelog
*    Thu Nov 1 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-3
-    Updated versions of cross toolchain components
*    Mon Oct 22 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-2
-    Replace _sysroot definition with sysroot
*    Fri Oct 19 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0
-    Initial build. First version
