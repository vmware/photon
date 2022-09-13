%global security_hardening nofortify

# It needs linux sources only to generate linux-api-headers for
# local glibc build. glibc bits get dropped and will not be packaged
%define linux_kernel_version 4.19.52
%define glibc_version 2.28

Name:    gcc-aarch64-linux-gnu
Summary: Cross GCC for Aarch64
Version: 7.3.0
Release: 3%{?dist}
Group:   Development/Tools
Vendor:  VMware, Inc.
Distribution: Photon
License: GPLv2+
URL:     http://gcc.gnu.org

Source0: https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
%define sha512  gcc=ad41a7e4584e40e92cdf860bc0288500fbaf5dfb7e8c3fcabe9eba809c87bcfa85b46c19c19921b0cdf6d05483faede8287bb9ea120c0d1559449a70e602c8d4
Source1: https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{linux_kernel_version}.tar.xz
%define sha512  linux=bc3ed347f6506a7a417865ead92a372107ded69db377dbde4344bb375f7ec5f53779334118927bf90b146d3286d5c51dc55998f09e93f944df3165b7fb440d7e
Source2: https://ftp.gnu.org/gnu/glibc/glibc-%{glibc_version}.tar.xz
%define sha512  glibc=521f820953ff07c69ece4c2186f59fc061a7f9747932cd70ef2995c2b2deee76eeb6de700d85071cdca5949179aa8ccee75eda7feca1394121ec7b821ad0a3f3
Source3: https://ftp.gnu.org/gnu/mpfr/mpfr-4.0.1.tar.gz
%define sha512  mpfr=d6b395febe034eb589fdcf503ed295f0e34d2c95de2685e7c4049bc1b3a84a78119c966b97fa1b77bbc047369a8623925479b1d90ed4794b6b37944aa137ca15
Source4: https://ftp.gnu.org/gnu/gmp/gmp-6.1.2.tar.xz
%define sha512  gmp=9f098281c0593b76ee174b722936952671fab1dae353ce3ed436a31fe2bc9d542eca752353f6645b7077c1f395ab4fdd355c58e08e2a801368f1375690eee2c6
Source5: https://ftp.gnu.org/gnu/mpc/mpc-1.1.0.tar.gz
%define sha512  mpc=72d657958b07c7812dc9c7cbae093118ce0e454c68a585bfb0e2fa559f1bf7c5f49b93906f580ab3f1073e5b595d23c6494d4d76b765d16dde857a18dd239628

Patch0:   libsanitizer-avoidustat.h-glibc-2.28.patch
Patch1:   PLUGIN_TYPE_CAST-gcc7.patch

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
# Using autosetup is not feasible
%setup -c -q
# Using autosetup is not feasible
%setup -q -T -D -q -a 1
# Using autosetup is not feasible
%setup -q -T -D -q -a 2
# Using autosetup is not feasible
%setup -q -T -D -q -a 3
# Using autosetup is not feasible
%setup -q -T -D -q -a 4
# Using autosetup is not feasible
%setup -q -T -D -q -a 5

cd gcc-%{version}
%autopatch -p1 -m0 -M1

ln -sf $(ls -1d ../mpfr-*/) mpfr
ln -sf $(ls -1d ../gmp-*) gmp
ln -sf $(ls -1d ../mpc-*/) mpc

# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

%build

%install

# Create usrmove symlinks
mkdir -p %{sysroot}%{_libdir} \
         %{sysroot}%{_bindir} \
         %{sysroot}%{_sbindir}

ln -sv usr/lib %{sysroot}/lib
ln -sv usr/bin %{sysroot}/bin
ln -sv usr/sbin %{sysroot}/sbin

###
### Step 1
###

echo "Step 1. Building Linux headers"

builddir=%{_builddir}/%{name}-%{version}
cd ${builddir}/linux-%{linux_kernel_version} && \
make mrproper %{?_smp_mflags} && \
make ARCH=%{target_linux_arch} headers_check %{?_smp_mflags} && \
make ARCH=%{target_linux_arch} \
     INSTALL_HDR_PATH=%{sysroot}%{_prefix} \
     headers_install %{?_smp_mflags}

###
### Step 2
###

echo "Step 2. Building GCC C compiler"

mkdir -p ${builddir}/build-gcc-%{target_arch} && \
cd ${builddir}/build-gcc-%{target_arch} && \
${builddir}/gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --target=%{target_arch} \
    --with-sysroot=%{sysroot} \
    --enable-plugins \
    --enable-languages=c \
    --enable-threads=posix \
    --enable-linker-build-id \
    --disable-multilib && \
make %{?_smp_mflags} all-gcc && \
make install-gcc %{?_smp_mflags}

###
### Step 3
###

echo "Step 3. Building GLIBC headers and C runtime"

mkdir -p ${builddir}/build-glibc-%{target_arch} && \
cd ${builddir}/build-glibc-%{target_arch} && \
${builddir}/glibc-%{glibc_version}/configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libdir}/glibc \
    --build=$MACHTYPE \
    --host=%{target_arch} \
    --target=%{target_arch} \
    --with-headers=%{sysroot}/usr/include \
    --disable-multilib \
    libc_cv_forced_unwind=yes && \
make install-bootstrap-headers=yes install-headers install_root=%{sysroot} %{?_smp_mflags} && \
make %{?_smp_mflags} csu/subdir_lib && \
mkdir -p %{sysroot}%{_libdir} && \
install csu/crt1.o csu/crti.o csu/crtn.o \
            %{sysroot}%{_libdir} && \
%{target_arch}-gcc \
    -nostdlib \
    -nostartfiles \
    -shared \
    -x c /dev/null \
    -o %{sysroot}%{_libdir}/libc.so && \
mkdir -p %{sysroot}/usr/include/gnu && \
touch %{sysroot}/usr/include/gnu/stubs.h

###
### Step 4
###

echo "Stage 4. Building GCC compiler support library"

cd ${builddir}/build-gcc-%{target_arch} && \
${builddir}/gcc-%{version}/configure \
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
make install-target-libgcc %{?_smp_mflags}
make %{?_smp_mflags} DESTDIR=%{buildroot} install-target-libgcc

###
### Step 5
###

echo "Step 5. Building full GLIBC"

cd ${builddir}/build-glibc-%{target_arch} && \
make %{?_smp_mflags} && \
make install install_root=%{sysroot} %{?_smp_mflags}

###
### Step 6
###

echo "Step 6. Building full GCC"

cd ${builddir}/build-gcc-%{target_arch} && \
make %{?_smp_mflags} all && \
make %{?_smp_mflags} DESTDIR=%{buildroot} install

CROSS_TOOLCHAIN_PKG_CONFIG=%{buildroot}%{_bindir}/%{target_arch}-pkg-config

cat > $CROSS_TOOLCHAIN_PKG_CONFIG << EOF
#! /bin/sh

SYSROOT=%{sysroot}

export PKG_CONFIG_DIR=
export PKG_CONFIG_LIBDIR=\${SYSROOT}%{_libdir}/pkgconfig:\${SYSROOT}/usr/share/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=\${SYSROOT}

exec pkg-config "\$@"
EOF
chmod +x $CROSS_TOOLCHAIN_PKG_CONFIG

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/gcc/*
%exclude %dir %{_libdir}/debug
%{_lib64dir}/*
%{_libexecdir}/*
%{_datadir}/*
%exclude %{_infodir}/dir
%{_prefix}/%{target_arch}/*

%changelog
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.3.0-3
- Fix binary path
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 7.3.0-2
- Fix build with new rpm
* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-1
- Cloned from cross-aarch64-tools.spec
* Thu Nov 1 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-3
- Updated versions of cross toolchain components
* Mon Oct 22 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0-2
- Replace _sysroot definition with sysroot
* Fri Oct 19 2018 Sriram Nambakam <snambakam@vmware.com> 1.0.0
- Initial build. First version
