%global security_hardening nofortify
%define _use_internal_dependency_generator 0
Summary:        Contains the GNU compiler collection
Name:           gcc-10
Version:        10.2.0
Release:        2%{?dist}
License:        GPLv2+
URL:            http://gcc.gnu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
%define sha512 gcc=42ae38928bd2e8183af445da34220964eb690b675b1892bbeb7cd5bb62be499011ec9a93397dba5e2fb681afadfc6f2767d03b9035b44ba9be807187ae6dc65e
Requires:       gmp
Requires:       mpfr
Requires:       mpc
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  mpc
BuildRequires:  zlib-devel

BuildRequires:  bison
%if 0%{?with_check}
BuildRequires:  autogen
BuildRequires:  dejagnu
%endif
# Do not provide any libraries as it will conflict with default system ones
AutoReqProv:    no

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

%prep
%autosetup -n gcc-%{version}

# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

%build

export glibcxx_cv_c99_math_cxx98=yes glibcxx_cv_c99_math_cxx11=yes
test %{_host} != %{_build} && export gcc_cv_objdump=%{_arch}-unknown-linux-gnu-objdump

%configure \
    $(test %{_host} != %{_build} && echo "--target=%{_host}") \
    --program-suffix=-10 \
    --enable-shared \
    --enable-threads=posix \
    --enable-__cxa_atexit \
    --enable-clocale=gnu \
    --enable-languages=c,c++ \
    --disable-multilib \
    --disable-bootstrap \
    --disable-libstdcxx-pch \
    --enable-linker-build-id \
    --enable-plugin \
    --with-system-zlib
%make_build

%install
%make_install DESTDIR=%{buildroot}
install -vdm 755 %{buildroot}/%_lib
ln -sv %{_bindir}/cpp-10 %{buildroot}/%{_lib}/cpp-10
ln -sv gcc-10 %{buildroot}%{_bindir}/cc-10
install -vdm 755 %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
mv -v %{buildroot}%{_lib64dir}/*gdb.py %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
chmod 755 %{buildroot}%{_lib64dir}/libgcc_s.so.1
mv %{buildroot}%{_lib64dir}/* %{buildroot}/usr/lib/gcc/%{_build}/%{version}/
rm -rf %{buildroot}%{_lib64dir} \
       %{buildroot}%{_infodir} \
       %{buildroot}%{_datadir}/locale

%if 0%{?with_check}
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

# No g++ failures
CPP_SUM_FILE=host-%{_host}/gcc/testsuite/g++/g++.sum
[ `grep ^FAIL $CPP_SUM_FILE | wc -l` -ne 0 -o `grep ^XPASS $CPP_SUM_FILE | wc -l` -ne 0 ] && exit 1 ||:
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_lib}/cpp-10
#   Executables
%{_bindir}/*
%exclude %{_libexecdir}/gcc/%{_arch}-unknown-linux-gnu/%{version}/f951
%{_libdir}/gcc/*
#   Library executables
%{_libexecdir}/gcc/*
#   Man pages
%{_mandir}/man1/gcov-10.1.gz
%{_mandir}/man1/gcov-dump-10.1.gz
%{_mandir}/man1/gcov-tool-10.1.gz
%{_mandir}/man1/gcc-10.1.gz
%{_mandir}/man1/g++-10.1.gz
%{_mandir}/man1/cpp-10.1.gz
%{_mandir}/man1/lto-dump-10.1.gz
%exclude %{_mandir}/man7/*.gz
%{_datadir}/gdb/*
%{_includedir}/c++/*
%dir %{_datarootdir}/gcc-%{version}/python/libstdcxx
%{_datarootdir}/gcc-%{version}/python/libstdcxx/*

%changelog
* Wed May 25 2022 Alexey Makhalov <amakhalov@vmware.com> 10.2.0-2
- Do not use auto provides.
* Fri May 13 2022 Alexey Makhalov <amakhalov@vmware.com> 10.2.0-1
- Alternative, higher version of gcc
