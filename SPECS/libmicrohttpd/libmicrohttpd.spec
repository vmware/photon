Name:           libmicrohttpd
Summary:        Lightweight library for embedding a webserver in applications
Version:        0.9.73
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://www.gnu.org/software/libmicrohttpd/
Source0:        https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
%define sha1    libmicrohttpd=5ff80818bbe3f8984e49809f4efeb2c38c7be232
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  autoconf, automake, libtool
BuildRequires:  gnutls-devel

Requires:       gnutls

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.
Key features that distinguish libmicrohttpd from other projects are:

%package devel
Summary:        Development files for libmicrohttpd
Requires:       %{name} = %{version}-%{release}
Requires:       gnutls-devel
%description devel
Development files for libmicrohttpd

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static --with-gnutls --enable-https=yes
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_bindir}/demo

%ldconfig_scriptlets

%files
%{_libdir}/libmicrohttpd.so.*

%files devel
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%{_datadir}/info/libmicrohttpd-tutorial.info.gz
%{_datadir}/info/libmicrohttpd.info.gz
%{_datadir}/info/libmicrohttpd_performance_data.png.gz
%{_datadir}/man/man3/libmicrohttpd.3.gz

%changelog
* Thu Aug 05 2021 Susant Sahani <ssahani@vmware.com> 0.9.73-2
- Modernize spec file. Use ldconfig scriptlets and autosetup
* Sun Apr 25 2021 Gerrit Photon <photon-checkins@vmware.com> 0.9.73-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.9.72-1
- Automatic Version Bump
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 0.9.71-2
- Requires gnutls-devel for installation
* Fri Aug 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.9.71-1
- Automatic Version Bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.9.70-1
- Initial rpm release
