Summary:        Zstandard - Fast real-time compression algorithm
Name:           zstd
Version:        1.3.5
Release:        1%{?dist}
URL:            https://github.com/facebook/zstd
License:        BSD
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/facebook/zstd/archive/%{name}-%{version}.tar.gz
%define sha1    zstd=c86b937a5534ced79e94dc043af835a6deed1115
%description
Zstandard - Fast real-time compression algorithm
%package    devel
Summary:    Header and development files for zstd
Requires:   %{name} = %{version}
%description    devel
Zstandard, or zstd as short version, is a fast lossless compression algorithm, targeting real-time compression scenarios at zlib-level and better compression ratios. It's backed by a very fast entropy stage, provided by Huff0 and FSE library.
%prep
%setup -q
%build
make V=1 %{?_smp_mflags}
%install
make prefix=%{buildroot}/usr install
install -vdm 755 %{buildroot}%{_lib}

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/unzstd
%{_bindir}/zstd
%{_bindir}/zstdcat
%{_bindir}/zstdgrep
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_mandir}/man1/*

%files devel
%{_includedir}/zbuff.h
%{_includedir}/zdict.h
%{_includedir}/zstd_errors.h
%{_includedir}/zstd.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.a
%{_libdir}/libzstd.so
%{_libdir}/libzstd.so.1
%{_libdir}/libzstd.so.1.3.5

%changelog
*   Wed Sep 26 2018 Sujay G <gsujay@vmware.com> 1.3.5
-   Initial build.
