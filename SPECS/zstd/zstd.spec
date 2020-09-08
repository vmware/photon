Summary:        Fast lossless compression algorithm
Name:           zstd
Version:        1.4.5
Release:        1%{?dist}
License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/facebook/zstd/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=9c344c2660c990b6d6a9cced73db3a0dfe2b0092

%description
Zstandard, or zstd as short version, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level and better compression
ratios. It's backed by a very fast entropy stage, provided by Huff0 and
FSE library.

%package devel
Summary:        Headers for building against zstd
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the headers necessary for building against the zstd
library, libzstd.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install PREFIX=%{_prefix} LIBDIR=%{_libdir}

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGELOG README.md
%{_bindir}/zstd*
%{_bindir}/unzstd
%{_libdir}/libzstd.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libzstd.so
%exclude %{_libdir}/libzstd.a
%{_libdir}/pkgconfig/libzstd.pc
%{_mandir}/man1/z*.1.gz
%{_mandir}/man1/unz*.1.gz

%changelog
*   Mon Sep 07 2020 Ankit Jain <ankitja@vmware.com> 1.4.5-1
-   Initial build. First version
