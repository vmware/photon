%global security_hardening nofortify
%define _use_internal_dependency_generator 0
%define program_suffix 12

Summary:        Contains the GNU compiler collection
Name:           gcc-12
Version:        12.3.0
Release:        1%{?dist}
License:        GPLv2+
URL:            http://gcc.gnu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
%define sha512 gcc=8fb799dfa2e5de5284edf8f821e3d40c2781e4c570f5adfdb1ca0671fcae3fb7f794ea783e80f01ec7bfbf912ca508e478bd749b2755c2c14e4055648146c204

Patch0: gcc-12-PLUGIN_TYPE_CAST.patch

Requires: gmp

%if 0%{?with_check}
BuildRequires: autogen
BuildRequires: dejagnu
%endif

# Do not provide any libraries as it will conflict with default system ones
AutoReqProv: no

# bison from publish RPMs will be used.
# We can't use BuildRequires here, as bison might not yet been built.
%define ExtraBuildRequires bison

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

%prep
%autosetup -p1 -n gcc-%{version}

# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

%build
export glibcxx_cv_c99_math_cxx98=yes glibcxx_cv_c99_math_cxx11=yes
test %{_host} != %{_build} && export gcc_cv_objdump=%{_arch}-unknown-linux-gnu-objdump

%configure \
    $(test %{_host} != %{_build} && echo "--target=%{_host}") \
    --program-suffix=-%{program_suffix} \
    --enable-shared \
    --enable-threads=posix \
    --enable-__cxa_atexit \
    --enable-clocale=gnu \
    --enable-languages=c,c++,fortran\
    --disable-multilib \
    --enable-default-pie \
    --enable-default-ssp \
    --disable-bootstrap \
    --disable-libstdcxx-pch \
    --enable-linker-build-id \
    --enable-plugin \
    --with-system-zlib

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_lib}
ln -srv %{buildroot}%{_bindir}/cpp-%{program_suffix} %{buildroot}%{_lib}
ln -sv gcc-%{program_suffix} %{buildroot}%{_bindir}/cc-%{program_suffix}
install -vdm 755 %{buildroot}%{_datadir}/gdb/auto-load%{_lib}
mv -v %{buildroot}%{_lib64dir}/*gdb.py %{buildroot}%{_datadir}/gdb/auto-load%{_lib}
chmod 755 %{buildroot}/%{_lib64dir}/libgcc_s.so.1
mv %{buildroot}%{_lib64dir}/* %{buildroot}%{_libdir}/gcc/%{_build}/%{version}/
rm -rf %{buildroot}%{_lib64dir} \
       %{buildroot}%{_infodir} \
       %{buildroot}%{_datadir}/locale

%check
ulimit -s 32768
# PCH tests fail with error: one ordd more PCH files were found, but they were invalid
# It happens if ASLR is on (due to bug in PCH)
# disable gcc PCH tests.
test `cat /proc/sys/kernel/randomize_va_space` -ne 0 && rm gcc/testsuite/gcc.dg/pch/pch.exp
# disable g++ PCH tests.
test `cat /proc/sys/kernel/randomize_va_space` -ne 0 && rm -rf gcc/testsuite/g++.dg/pch
# This test fails with warning:
#   In file included from /usr/src/photon/BUILD/gcc-10.2.0/gcc/testsuite/gcc.dg/asan/pr80166.c:5:
#   /usr/include/unistd.h:701:12: note: in a call to function 'getgroups' declared with attribute 'write_only (2, 1)'
#   /usr/src/photon/BUILD/gcc-10.2.0/gcc/testsuite/gcc.dg/asan/pr80166.c:19:7: warning: argument 1 value -1 is negative [-Wstringop-overflow=]
# Ignore it.
rm gcc/testsuite/gcc.dg/asan/pr80166.c
# Skip two c++ tests
rm gcc/testsuite/g++.dg/coroutines/torture/co-ret-17-void-ret-coro.C
rm gcc/testsuite/g++.dg/coroutines/torture/pr95519-05-gro.C
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs

# run only gcc tests
make %{?_smp_mflags} check-gcc

# No gcc failures
GCC_SUM_FILE=host-%{_host}/gcc/testsuite/gcc/gcc.sum
[ `grep ^FAIL $GCC_SUM_FILE | wc -l` -ne 0 -o `grep ^XPASS $GCC_SUM_FILE | wc -l` -ne 0 ] && exit 1 ||:

# 1 g++ fail
CPP_SUM_FILE=host-%{_host}/gcc/testsuite/g++/g++.sum
[ `grep ^FAIL $CPP_SUM_FILE | wc -l` -ne 1 -o `grep ^XPASS $CPP_SUM_FILE | wc -l` -ne 0 ] && exit 1 ||:
[ `grep "^FAIL: g++.dg/asan/asan_test.C   -O2  (test for excess errors)" $CPP_SUM_FILE | wc -l` -ne 1 ] && exit 1 ||:

# 1 gfortran fail
GFORTRAN_SUM_FILE=host-%{_host}/gcc/testsuite/gfortran/gfortran.sum
[ `grep ^FAIL $GFORTRAN_SUM_FILE | wc -l` -ne 1 -o `grep ^XPASS $GFORTRAN_SUM_FILE | wc -l` -ne 0 ] && exit 1 ||:
[ `grep "^FAIL: gfortran.dg/analyzer/pr93993.f90   -O  (test for excess errors)" $GFORTRAN_SUM_FILE | wc -l` -ne 1 ] && exit 1 ||:

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_lib}/cpp-%{program_suffix}
%{_bindir}/*
%exclude %{_libexecdir}/gcc/%{_arch}-unknown-linux-gnu/%{version}/f951
%{_libdir}/gcc/*
# Library executables
%{_libexecdir}/gcc/*
# Man pages
%{_mandir}/man1/gcov-%{program_suffix}.1.gz
%{_mandir}/man1/gcov-dump-%{program_suffix}.1.gz
%{_mandir}/man1/gcov-tool-%{program_suffix}.1.gz
%{_mandir}/man1/gcc-%{program_suffix}.1.gz
%{_mandir}/man1/g++-%{program_suffix}.1.gz
%{_mandir}/man1/cpp-%{program_suffix}.1.gz
%{_mandir}/man1/lto-dump-%{program_suffix}.1.gz
%{_mandir}/man7/*.gz
%{_datadir}/gdb/*
%{_mandir}/man1/gfortran-%{program_suffix}.1.gz
%{_libexecdir}/gcc/%{_arch}-unknown-linux-gnu/%{version}/f951
%dir %{_datadir}/gcc-%{version}/python/libstdcxx
%{_datadir}/gcc-%{version}/python/libstdcxx/*
%{_includedir}/c++/*

%changelog
* Wed Jan 17 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 12.3.0-1
- Alternative, higher version of gcc
