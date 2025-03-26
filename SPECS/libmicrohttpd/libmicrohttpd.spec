Name:           libmicrohttpd
Summary:        Lightweight library for embedding a webserver in applications
Version:        0.9.76
Release:        4%{?dist}
URL:            http://www.gnu.org/software/libmicrohttpd/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.9.76-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.9.76-3
- Release bump for SRP compliance
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.76-2
- Bump version as a part of gnutls upgrade
* Wed Sep 13 2023 Srish Srinivasan <ssrish@vmware.com> 0.9.76-1
- Update to v0.9.76 to fix CVE-2023-27371
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.9.75-2
- Bump version as a part of gnutls upgrade
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
