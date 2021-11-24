Summary:        Fast lossless compression algorithm
Name:           zstd
Version:        1.5.2
Release:        1%{?dist}
License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/facebook/zstd/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=e107508a41fca50845cc2494e64adaba93efb95a2fa486fc962510a8ba4b2180d93067cae9870f119e88e5e8b28a046bc2240b0b23cdd8933d1fb1a6a9668c1e
Requires:       zstd-libs = %{version}-%{release}

%description
Zstandard, or zstd as short version, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level and better compression
ratios. It's backed by a very fast entropy stage, provided by Huff0 and
FSE library.

%package      libs
Summary:      Zstd shared library
Group:        System/Libraries

%description libs
This subpackage contains the implementation as a shared library.

%package devel
Summary:        Headers for building against zstd
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(libzstd)
Requires:       glibc-devel

%description devel
This package contains the headers necessary for building against the zstd
library, libzstd.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

%check
make %{?_smp_mflags} check

%post -n zstd-libs -p /sbin/ldconfig
%postun -n zstd-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGELOG README.md
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
%doc LICENSE

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
*   Wed Jul 20 2022 Harinadh D <hdommaraju@vmware.com> 1.5.2-1
-   Fix CVE-2021-24032 and version update
*   Thu Oct 15 2020 Anisha Kumari <kanisha@vmware.com> 1.4.5-2
-   Added package libs for zstd and files.
*   Mon Sep 07 2020 Ankit Jain <ankitja@vmware.com> 1.4.5-1
-   Initial build. First version
