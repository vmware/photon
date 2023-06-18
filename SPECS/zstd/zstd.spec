Summary:        Fast lossless compression algorithm
Name:           zstd
Version:        1.5.5
Release:        2%{?dist}
License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/facebook/zstd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=356994e0d8188ce97590bf86b602eb50cbcb2f951594afb9c2d6e03cc68f966862505afc4a50e76efd55e4cfb11dbc9b15c7837b7827a961a1311ef72cd23505

Requires:       zstd-libs = %{version}-%{release}

%description
Zstandard, or zstd as short version, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level and better compression
ratios. It's backed by a very fast entropy stage, provided by Huff0 and
FSE library.

%package        libs
Summary:        Zstd shared library
Group:          System/Libraries

%description    libs
This subpackage contains the implementation as a shared library.

%package        devel
Summary:        Headers for building against zstd
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(libzstd)
Requires:       glibc-devel

%description    devel
This package contains the headers necessary for building against the zstd
library, libzstd.

%prep
%autosetup -p1

%build
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} %{?_smp_mflags}

%check
%make_build check

%post -n zstd-libs -p /sbin/ldconfig
%postun -n zstd-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/zstd
%{_bindir}/zstdcat
%{_bindir}/zstdgrep
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_bindir}/unzstd
%{_mandir}/man1/zstd.1*
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstdcat.1*
%{_mandir}/man1/zstdgrep.1.*
%{_mandir}/man1/zstdless.1.*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libzstd.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so
%exclude %{_libdir}/libzstd.a

%changelog
* Fri Dec 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.5.5-2
- Generate pc file properly
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com>  1.5.5-1
- Upgrade to v1.5.5
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-1
- Upgrade to v1.5.2
* Thu Oct 15 2020 Anisha Kumari <kanisha@vmware.com> 1.4.5-2
- Added package libs for zstd and files.
* Mon Sep 07 2020 Ankit Jain <ankitja@vmware.com> 1.4.5-1
- Initial build. First version
