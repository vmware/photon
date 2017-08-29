%define _use_internal_dependency_generator 0
Summary:        Contains the GNU compiler collection
Name:           gcc
Version:        6.3.0
Release:        4%{?dist}
License:        GPLv2+
URL:            http://gcc.gnu.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.gnu.org/gnu/gcc/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha1 gcc=928ab552666ee08eed645ff20ceb49d139205dea
Patch0:         PLUGIN_TYPE_CAST.patch
Requires:       libstdc++-devel = %{version}-%{release}
Requires:       libgcc-devel = %{version}-%{release}
Requires:       libgomp-devel = %{version}-%{release}
Requires:       libgcc-atomic = %{version}-%{release}
Requires:       gmp
%if %{with_check}
BuildRequires:  autogen
BuildRequires:  dejagnu
%endif

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
%setup -q
%patch0 -p1

# disable FORTIFY_SOURCE=2 from hardening
sed -i '/*cpp:/s/^/# /' `dirname $(gcc --print-libgcc-file-name)`/../specs
sed -i '/Ofast:-D_FORTIFY_SOURCE=2/s/^/# /' `dirname $(gcc --print-libgcc-file-name)`/../specs
# disable no-pie for gcc binaries
sed -i '/^NO_PIE_CFLAGS = /s/@NO_PIE_CFLAGS@//' gcc/Makefile.in

install -vdm 755 ../gcc-build
%build

# Fix compilation issue for glibc-2.26.
# TODO: remove these lines after gcc update to 7.2+
#
# 1. "typedef struct ucontext ucontext_t" was renamed to
#    "typedef struct ucontext_t ucontext_t"
sed -i 's/struct ucontext/ucontext_t/g' libgcc/config/i386/linux-unwind.h
# 2. struct sigaltstack removed
sed -i 's/struct sigaltstack/void/g' libsanitizer/sanitizer_common/sanitizer_linux.cc
sed -i '/struct sigaltstack;/d' libsanitizer/sanitizer_common/sanitizer_linux.h
sed -i 's/struct sigaltstack/void/g' libsanitizer/sanitizer_common/sanitizer_linux.h
sed -i 's/struct sigaltstack/stack_t/g' libsanitizer/sanitizer_common/sanitizer_stoptheworld_linux_libcdep.cc
sed -i 's/__res_state/struct __res_state/g' libsanitizer/tsan/tsan_platform_linux.cc

export glibcxx_cv_c99_math_cxx98=yes glibcxx_cv_c99_math_cxx11=yes

cd ../gcc-build
SED=sed \
../%{name}-%{version}/configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --enable-threads=posix \
    --enable-__cxa_atexit \
    --enable-clocale=gnu \
    --enable-languages=c,c++,fortran\
    --disable-multilib \
    --disable-bootstrap \
    --enable-linker-build-id \
    --enable-plugin \
    --with-system-zlib
#   --disable-silent-rules
make
%install
pushd ../gcc-build
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%_lib
ln -sv %{_bindir}/cpp %{buildroot}/%{_lib}
ln -sv gcc %{buildroot}%{_bindir}/cc
install -vdm 755 %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
%ifarch x86_64
    mv -v %{buildroot}%{_lib64dir}/*gdb.py %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
%else
    mv -v %{buildroot}%{_libdir}/*gdb.py %{buildroot}%{_datarootdir}/gdb/auto-load%{_lib}
%endif
rm -rf %{buildroot}%{_infodir}
popd
%find_lang %{name} --all-name

%check
ulimit -s 32768
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
# run only gcc tests
cd ../gcc-build/gcc
make %{?_smp_mflags} check-gcc
# print summary first
tail testsuite/gcc/gcc.sum
# ignore exit code and check for expected number of failures: 493
tail testsuite/gcc/gcc.sum  | grep "# of unexpected failures.*493"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_lib}/cpp
#   Executables
%exclude %{_bindir}/*gfortran
%exclude %{_libexecdir}/gcc/x86_64-pc-linux-gnu/%{version}/f951
%{_bindir}/*
#   Libraries
%ifarch x86_64
%{_lib64dir}/*
%endif
%{_libdir}/gcc/*
#   Library executables
%{_libexecdir}/gcc/*
#   Man pages
%{_mandir}/man1/gcov.1.gz
%{_mandir}/man1/gcc.1.gz
%{_mandir}/man1/g++.1.gz
%{_mandir}/man1/cpp.1.gz
%{_mandir}/man7/*.gz
%{_datadir}/gdb/*

%ifarch x86_64
%exclude %{_lib64dir}/libgcc*
%exclude %{_lib64dir}/libstdc++*
%exclude %{_lib64dir}/libgomp*
%else
%exclude %{_libdir}/libgcc*
%exclude %{_libdir}/libstdc++*
%exclude %{_libdir}/libgomp*
%endif

%files -n     gfortran
%defattr(-,root,root)
%{_bindir}/*gfortran
%{_mandir}/man1/gfortran.1.gz
%{_libexecdir}/gcc/x86_64-pc-linux-gnu/%{version}/f951

%files -n libgcc
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libgcc_s.so.*
%else
%{_libdir}/libgcc_s.so.*
%endif

%files -n libgcc-atomic
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libatomic.so*
%else
%{_lib64dir}/libatomic.so*
%endif

%files -n libgcc-devel
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libgcc_s.so
%else
%{_libdir}/libgcc_s.so
%endif


%files -n libstdc++
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libstdc++.so.*
%else
%{_libdir}/libstdc++.so.*
%endif
%dir %{_datarootdir}/gcc-%{version}/python/libstdcxx
%{_datarootdir}/gcc-%{version}/python/libstdcxx/*

%files -n libstdc++-devel
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libstdc++.so
%{_lib64dir}/libstdc++.la
%else
%{_libdir}/libstdc++.so
%{_libdir}/libstdc++.la
%endif

%{_includedir}/c++/*

%files -n libgomp
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libgomp*.so.*
%else
%{_libdir}/libgomp*.so.*
%endif

%files -n libgomp-devel
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/libgomp.a
%{_lib64dir}/libgomp.la
%{_lib64dir}/libgomp.so
%{_lib64dir}/libgomp.spec
%else
%{_libdir}/libgomp.a
%{_libdir}/libgomp.la
%{_libdir}/libgomp.so
%{_libdir}/libgomp.spec
%endif

%changelog
*   Mon Aug 28 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-4
-   Fix makecheck to track # of known failures
*   Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-3
-   Fix compilation issue for glibc-2.26
*   Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-2
-   Improve make check
*   Thu Mar 9 2017 Alexey Makhalov <amakhalov@vmware.com> 6.3.0-1
-   Update version to 6.3
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 5.3.0-6
-   Enabled fortran.
*   Wed Feb 22 2017 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-5
-   Added new plugin entry point: PLUGIN_TYPE_CAST (.patch)
*   Thu Sep  8 2016 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-4
-   Enable plugins and linker build id.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.0-3
-   GA - Bump release of all rpms
*   Tue May 17 2016 Anish Swaminathan <anishs@vmware.com> 5.3.0-2
-   Change package dependencies
*   Mon Mar 28 2016 Alexey Makhalov <amakhalov@vmware.com> 5.3.0-1
-   Update version to 5.3
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 4.8.2-6
-   Handled locale files with macro find_lang
*   Mon Nov 02 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.8.2-5
-   Put libatomic.so into its own package.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 4.8.2-4
-   Updated group.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 4.8.2-3
-   Update according to UsrMove.
*   Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 4.8.2-2
-   Packaging .la files
*   Tue Apr 01 2014 baho-utot <baho-utot@columbus.rr.com> 4.8.2-1
-   Initial build. First version
