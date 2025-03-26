%global security_hardening nofortify
%define _use_internal_dependency_generator 0

Summary:        Contains the GNU compiler collection
Name:           gcc
Version:        12.2.0
Release:        5%{?dist}
URL:            http://gcc.gnu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/gcc/%{name}-%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0:         PLUGIN_TYPE_CAST.patch

Requires:       libstdc++-devel = %{version}-%{release}
Requires:       libgcc-devel = %{version}-%{release}
Requires:       libgomp-devel = %{version}-%{release}
Requires:       libgcc-atomic = %{version}-%{release}
Requires:       gmp

%if 0%{?with_check}
BuildRequires:  autogen
BuildRequires:  dejagnu
%endif

Provides: gcc-10
Obsoletes: gcc-10

# bison from publish RPMs will be used.
# We can't use BuildRequires here, as bison might not yet been built.
%define ExtraBuildRequires bison

%description
The GCC package contains the GNU compiler collection,
which includes the C and C++ compilers.

%package -n     gfortran
Summary:        GNU Fortran compiler.
Group:          Development/Tools
%description -n gfortran
The gfortran package contains GNU Fortran compiler.

%package -n     libgcc
Summary:    GNU C Library
Group:          System Environment/Libraries
%description -n libgcc
The libgcc package contains GCC shared libraries for gcc.

%package -n     libgcc-atomic
Summary:        GNU C Library for atomic counter updates
Group:          System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
%description -n libgcc-atomic
The libgcc package contains GCC shared libraries for atomic counter updates.

%package -n     libgcc-devel
Summary:        GNU C Library
Group:          Development/Libraries
Requires:       libgcc = %{version}-%{release}
%description -n libgcc-devel
The libgcc package contains GCC shared libraries for gcc .
This package contains development headers and static library for libgcc.

%package -n     libstdc++
Summary:        GNU C Library
Group:          System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
%description -n libstdc++
This package contains the GCC Standard C++ Library v3, an ongoing project to implement the ISO/IEC 14882:1998 Standard C++ library.

%package -n     libstdc++-devel
Summary:        GNU C Library
Group:          Development/Libraries
Requires:       libstdc++ = %{version}-%{release}
%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.
This package includes the headers files and libraries needed for C++ development.

%package -n     libgomp
Summary:        GNU C Library
Group:          System Environment/Libraries
%description -n libgomp
An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.

%package -n     libgomp-devel
Summary:        Development headers and static library for libgomp
Group:          Development/Libraries
Requires:       libgomp = %{version}-%{release}
%description -n libgomp-devel
An implementation of OpenMP for the C, C++, and Fortran 95 compilers in the GNU Compiler Collection.
This package contains development headers and static library for libgomp

%prep
%autosetup -p1

# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

%build
export glibcxx_cv_c99_math_cxx98=yes glibcxx_cv_c99_math_cxx11=yes
test %{_host} != %{_build} && export gcc_cv_objdump=%{_arch}-unknown-linux-gnu-objdump

%configure \
    $(test %{_host} != %{_build} && echo "--target=%{_host}") \
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
ln -sv %{_bindir}/cpp %{buildroot}%{_lib}
ln -sv gcc %{buildroot}%{_bindir}/cc
install -vdm 755 %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
mv -v %{buildroot}%{_lib64dir}/*gdb.py %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
chmod 755 %{buildroot}/%{_lib64dir}/libgcc_s.so.1
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

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

%files -f %{name}.lang
%defattr(-,root,root)
%{_lib}/cpp
#   Executables
%exclude %{_bindir}/*gfortran
%{_bindir}/*
#   Libraries
%{_lib64dir}/*
%exclude %{_libexecdir}/gcc/%{_arch}-unknown-linux-gnu/%{version}/f951
%{_libdir}/gcc/*
#   Library executables
%{_libexecdir}/gcc/*
#   Man pages
%{_mandir}/man1/gcov.1.gz
%{_mandir}/man1/gcov-dump.1.gz
%{_mandir}/man1/gcov-tool.1.gz
%{_mandir}/man1/gcc.1.gz
%{_mandir}/man1/g++.1.gz
%{_mandir}/man1/cpp.1.gz
%{_mandir}/man1/lto-dump.1.gz
%{_mandir}/man7/*.gz
%{_datadir}/gdb/*

%exclude %{_lib64dir}/libgcc*
%exclude %{_lib64dir}/libstdc++*
%exclude %{_lib64dir}/libgomp*

%files -n     gfortran
%defattr(-,root,root)
%{_bindir}/*gfortran
%{_mandir}/man1/gfortran.1.gz
%{_libexecdir}/gcc/%{_arch}-unknown-linux-gnu/%{version}/f951

%files -n libgcc
%defattr(-,root,root)
%{_lib64dir}/libgcc_s.so.*

%files -n libgcc-atomic
%defattr(-,root,root)
%{_lib64dir}/libatomic.so*

%files -n libgcc-devel
%defattr(-,root,root)
%{_lib64dir}/libgcc_s.so

%files -n libstdc++
%defattr(-,root,root)
%{_lib64dir}/libstdc++.so.*
%dir %{_datarootdir}/gcc-%{version}/python/libstdcxx
%{_datarootdir}/gcc-%{version}/python/libstdcxx/*

%files -n libstdc++-devel
%defattr(-,root,root)
%{_lib64dir}/libstdc++.so
%{_lib64dir}/libstdc++.a

%{_includedir}/c++/*

%files -n libgomp
%defattr(-,root,root)
%{_lib64dir}/libgomp*.so.*

%files -n libgomp-devel
%defattr(-,root,root)
%{_lib64dir}/libgomp.a
%{_lib64dir}/libgomp.so
%{_lib64dir}/libgomp.spec

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 12.2.0-5
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 12.2.0-4
- Remove standalone license exceptions
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 12.2.0-3
- Bump version to generate SRP provenance file
* Tue Dec 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 12.2.0-2
- Add provides & obsolets gcc-10
* Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 12.2.0-1
- Version update
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 10.2.0-2
- Remove .la files
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 10.2.0-1
- Version update
* Wed Jan 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.4.0-2
- Bump version with new openssl in publish rpms
* Thu May 07 2020 Alexey Makhalov <amakhalov@vmware.com> 8.4.0-1
- Version update
* Tue Mar 24 2020 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-6
- Fix compilation issue with glibc-2.31
* Tue Nov 06 2018 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-5
- Cross compilation support
* Fri Nov 02 2018 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-4
- Use nofortify security_hardening instead of sed hacking
- Use %configure
* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 7.3.0-3
- Fix compilation issue for glibc-2.28
* Thu Aug 30 2018 Keerthana K <keerthanak@vmware.com> 7.3.0-2
- Packaging .a files (libstdc++-static files).
* Wed Aug 01 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 7.3.0-1
- Update to version 7.3.0 to get retpoline support.
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-7
- Aarch64 support
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-6
- Added smp_mflags for parallel build
* Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-5
- Enable elfdeps for libgcc_s to generate libgcc_s.so.1(*)(64bit) provides
* Mon Aug 28 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-4
- Fix makecheck
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-3
- Fix compilation issue for glibc-2.26
* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-2
- Improve make check
* Thu Mar 9 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-1
- Update version to 6.3
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 5.3.0-6
- Enabled fortran.
* Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-5
- Added new plugin entry point: PLUGIN_TYPE_CAST (.patch)
* Thu Sep  8 2016 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-4
- Enable plugins and linker build id.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.0-3
- GA - Bump release of all rpms
* Tue May 17 2016 Anish Swaminathan <anishs@vmware.com> 5.3.0-2
- Change package dependencies
* Mon Mar 28 2016 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-1
- Update version to 5.3
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 4.8.2-6
- Handled locale files with macro find_lang
* Mon Nov 02 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.8.2-5
- Put libatomic.so into its own package.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 4.8.2-4
- Updated group.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 4.8.2-3
- Update according to UsrMove.
* Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 4.8.2-2
- Packaging .la files
* Tue Apr 01 2014 baho-utot <baho-utot@columbus.rr.com> 4.8.2-1
- Initial build. First version
