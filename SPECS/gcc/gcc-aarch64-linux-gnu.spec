%global security_hardening nofortify

# It needs linux sources only to generate linux-api-headers for
# local glibc build. glibc bits get dropped and will not be packaged
%define linux_kernel_version 4.19.52
%define glibc_version 2.28

Name:    gcc-aarch64-linux-gnu
Summary: Cross GCC for Aarch64
Version: 7.3.0
Release: 1%{?dist}
Group:   Development/Tools
Vendor:  VMware, Inc.
Distribution: Photon
License: GPLv2+
URL:     http://gcc.gnu.org
Source0: https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
%define sha1 gcc=9689b9cae7b2886fdaa08449a26701f095c04e48
Source1: https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{linux_kernel_version}.tar.xz
%define sha1 linux=0fc8eeba8a8a710c95d71f140dfdc4bdff735248
Source2: https://ftp.gnu.org/gnu/glibc/glibc-%{glibc_version}.tar.xz
%define sha1 glibc=ccb5dc9e51a9884df8488f86982439d47b283b2a
Source3: https://ftp.gnu.org/gnu/mpfr/mpfr-4.0.1.tar.gz
%define sha1 mpfr=655e3cf416a0cc9530d9cb3c38dc8839504f0e98
Source4: https://ftp.gnu.org/gnu/gmp/gmp-6.1.2.tar.xz
%define sha1 gmp=9dc6981197a7d92f339192eea974f5eca48fcffe
Source5: https://ftp.gnu.org/gnu/mpc/mpc-1.1.0.tar.gz
%define sha1 mpc=b019d9e1d27ec5fb99497159d43a3164995de2d0
Patch0:   libsanitizer-avoidustat.h-glibc-2.28.patch
Patch1:   PLUGIN_TYPE_CAST.patch
BuildArch: x86_64
Provides: libgcc_s.so.1
Provides: libgcc_s.so.1(GCC_3.0)
Provides: libgcc_s.so.1(GCC_3.3)
Provides: libgcc_s.so.1(GCC_4.2.0)
Provides: libgcc_s.so.1(GLIBC_2.0)
BuildRequires: binutils-aarch64-linux-gnu
Requires: binutils-aarch64-linux-gnu

%global target_arch aarch64-unknown-linux-gnu
%global target_linux_arch arm64
%global sysroot /target-aarch64

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

%prep
%setup -c -q
%setup -T -D -q -a 1
%setup -T -D -q -a 2
%setup -T -D -q -a 3
%setup -T -D -q -a 4
%setup -T -D -q -a 5

cd gcc-%{version}
%patch0 -p1
%patch1 -p1
ln -sf `ls -1d ../mpfr-*/` mpfr
ln -sf `ls -1d ../gmp-*/` gmp
ln -sf `ls -1d ../mpc-*/` mpc

# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

%build

# Create usrmove symlinks
mkdir -p %{sysroot}/usr/lib && ln -s usr/lib %{sysroot}/lib
mkdir -p %{sysroot}/usr/bin && ln -s usr/bin %{sysroot}/bin
mkdir -p %{sysroot}/usr/sbin && ln -s usr/sbin %{sysroot}/sbin

builddir=$RPM_BUILD_DIR/%{name}-%{version}

###
### Step 1
###

echo "Step 1. Building Linux headers"

cd $builddir/linux-%{linux_kernel_version} && \
make mrproper && \
make ARCH=%{target_linux_arch} headers_check && \
make ARCH=%{target_linux_arch} \
     INSTALL_HDR_PATH=%{sysroot}%{_prefix} \
     headers_install

###
### Step 2
###

echo "Step 2. Building GCC C compiler"

mkdir -p $builddir/build-gcc-%{target_arch} && \
cd $builddir/build-gcc-%{target_arch} && \
$builddir/gcc-%{version}/configure \
    --prefix=%{_prefix} \
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
### Step 3
###

echo "Step 3. Building GLIBC headers and C runtime"

mkdir -p $builddir/build-glibc-%{target_arch} && \
cd $builddir/build-glibc-%{target_arch} && \
$builddir/glibc-%{glibc_version}/configure \
    --prefix=%{_prefix} \
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
### Step 4
###

echo "Stage 4. Building GCC compiler support library"

cd $builddir/build-gcc-%{target_arch} && \
$builddir/gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --enable-shared \
    --enable-threads=posix \
    --enable-__cxa_atexit \
    --enable-clocale=gnu \
    --enable-languages=c,c++,fortran \
    --disable-multilib \
    --enable-linker-build-id \
    --enable-plugin \
    --with-system-zlib && \
make %{?_smp_mflags} all-target-libgcc && \
make install-target-libgcc
make %{?_smp_mflags} DESTDIR=%{buildroot} install-target-libgcc

###
### Step 5
###

echo "Step 5. Building full GLIBC"

cd $builddir/build-glibc-%{target_arch} && \
make %{?_smp_mflags} && \
make install install_root=%{sysroot}

###
### Step 6
###

echo "Step 6. Building full GCC"

cd $builddir/build-gcc-%{target_arch} && \
make %{?_smp_mflags} all && \
make %{?_smp_mflags} DESTDIR=%{buildroot} install


%install

CROSS_TOOLCHAIN_PKG_CONFIG=%{buildroot}%{_bindir}/%{target_arch}-pkg-config

cat > $CROSS_TOOLCHAIN_PKG_CONFIG << EOF
#! /bin/sh

SYSROOT=%{sysroot}

export PKG_CONFIG_DIR=
export PKG_CONFIG_LIBDIR=\${SYSROOT}/usr/lib/pkgconfig:\${SYSROOT}/usr/share/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=\${SYSROOT}

exec pkg-config "\$@"
EOF
chmod +x $CROSS_TOOLCHAIN_PKG_CONFIG

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug
%{_lib64dir}/*
%{_libexecdir}/*
%{_datadir}/*
%exclude %{_datadir}/info/dir
%{_prefix}/%{target_arch}/*

%changelog
* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-1
- Cloned from cross-aarch64-tools.spec
* Thu Nov 1 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-3
- Updated versions of cross toolchain components
* Mon Oct 22 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-2
- Replace _sysroot definition with sysroot
* Fri Oct 19 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0
- Initial build. First version
