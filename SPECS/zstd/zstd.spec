Summary:      Zstandard compression library
Name:         zstd
Version:      1.4.5
Release:      2%{?dist}
License:      BSD and GPLv2
URL:          https://github.com/facebook/zstd
Group:        Productivity/Archiving/Compression
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://github.com/facebook/zstd/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  zstd=b03c497c3e0590c3d384cb856e3024f144b2bfac0d805d80e68deafa612c68237f12a2d657416d476a28059e80936c79f099fc42331464b417593895ea214387
Patch0:       zstd-CVE-2021-24032.patch
Requires:     zstd-libs = %{version}-%{release}

%description
Zstandard is fast lossless compression algorithm, targeting real-time \
compression scenarios at zlib-level and better compression ratios.

%package      libs
Summary:      Zstd shared library
Group:        System/Libraries

%description libs
This subpackage contains the implementation as a shared library.

%package     devel
Summary:     Development files for Zstd compression library
Group:       Development/Libraries/C and C++
Requires:    zstd = %{version}-%{release}
Provides:    pkgconfig(libzstd)
Requires:    glibc-devel

%description devel
Needed for compiling programs that link with the library, \
contain Header files for Zstd library.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build %{?_smp_mflags}

%install
%make_install PREFIX=%{_prefix} %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post -n zstd-libs -p /sbin/ldconfig
%postun -n zstd-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
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
%{_includedir}/zbuff.h
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so
%exclude %{_libdir}/libzstd.a

%changelog
* Fri Jul 08 2022 HArinadh D <hdommaraju@vmware.com> 1.4.5-2
- fix CVE-2021-24032
* Tue Sep 8 2020 Anisha Kumari <kanisha@vmware.com> 1.4.5-1
- Initial packaging
