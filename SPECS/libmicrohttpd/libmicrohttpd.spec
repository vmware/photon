Name:           libmicrohttpd
Summary:        Lightweight library for embedding a webserver in applications
Version:        0.9.75
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://www.gnu.org/software/libmicrohttpd/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
%define sha512  %{name}=4dc62ed191342a61cc2767171bb1ff4050f390db14ef7100299888237b52ea0b04b939c843878fe7f5daec2b35a47b3c1b7e7c11fb32d458184fe6b19986a37c

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
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

%description    devel
Development files for libmicrohttpd

%prep
%autosetup

%build
autoreconf -fi
%configure --disable-static --with-gnutls --enable-https=yes
%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.la \
      %{buildroot}%{_infodir}/dir \
      %{buildroot}%{_bindir}/demo

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
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.9.75-1
- Automatic Version Bump
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
- Initial rpm release.
