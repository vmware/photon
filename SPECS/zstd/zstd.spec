Summary:      Zstandard compression library
Name:         zstd
Version:      1.4.5
Release:      1%{?dist}
License:      BSD and GPLv2
URL:          https://github.com/facebook/zstd
Group:        Productivity/Archiving/Compression
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://github.com/facebook/zstd/archive/v{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha1  zstd=9c344c2660c990b6d6a9cced73db3a0dfe2b0092
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
%setup -q
find -name .gitignore -delete

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install PREFIX=%{_prefix} LIBDIR=%{_libdir}

%check
make check

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
* Tue Sep 8 2020 Anisha Kumari <kanisha@vmware.com> 1.4.5-1
- Initial packaging
