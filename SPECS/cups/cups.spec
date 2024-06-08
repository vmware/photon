Summary:        The Common UNIX Printing System
Name:           cups
Version:        2.4.7
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://openprinting.github.io/cups
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/OpenPrinting/cups/releases/download/v%{version}/cups-%{version}.tar.gz
%define sha512 %{name}=27ca505a2868aa7bc248bac892aafe2a837633e73b6059d3ab4812264e3b0e786ef075751e8cc4300ce6bc43ef095e3d77dd3fce88ce8e72ca69b65093427bca
Patch0:         0001-Fix-domain-socket-handling.patch

BuildRequires:  automake
BuildRequires:  dbus-devel
BuildRequires:  pkg-config
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  libusb-devel
BuildRequires:  openssl-devel

Requires:       libusb
Requires:       dbus
Requires:       gnutls
Requires:       krb5
Requires:       zlib

%description
The Common Unix Printing System (CUPS) is a print spooler and associated utilities.
It is based on the "Internet Printing Protocol" and provides printing services to most PostScript and raster printers.

%package devel
Summary: Header and development files
License: LGPLv2
Group:   Development/Libraries/C and C++
Requires: %{name} = %{version}-%{release}

%description devel
It contains the header files to create applications

%prep
%autosetup -p1

%build
%configure \
        CFLAGS="%{optflags}" \
        CXXFLAGS="%{optflags}"

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install BUILDROOT=%{buildroot}
find %{buildroot} -name '*.desktop' -delete
find %{buildroot} -name '*.png' -delete

%ldconfig_scriptlets

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/cups/cups-files.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/cups/cupsd.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/cups/snmp.conf
%config %{_sysconfdir}/cups/cupsd.conf.default
%config %{_sysconfdir}/cups/cups-files.conf.default
%config %{_sysconfdir}/cups/snmp.conf.default
%dir %attr(755,root,root) %{_sysconfdir}/cups/ppd
%dir %attr(700,root,root) %{_sysconfdir}/cups/ssl
%config %{_sysconfdir}/rc.d/
%config %{_sysconfdir}/dbus-1/system.d/cups.conf

%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libcups*.so.*
%dir %{_libdir}/cups
%{_libdir}/cups/*

%doc %{_mandir}/*
%doc %{_defaultdocdir}/cups
%{_datadir}/cups/
%{_datadir}/locale/

%files devel
%defattr(-,root,root)
%{_includedir}/cups/
%{_libdir}/libcups*.so
%{_libdir}/pkgconfig/cups.pc

%changelog
* Thu Jun 06 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.4.7-3
- Fix CVE-2024-35235
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.7-2
- Bump version as a part of gnutls upgrade
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 2.4.7-1
- Update to v2.4.7 to fix CVE-2023-4504
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.6-1
- Update to v2.4.6
* Thu Jun 15 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2.7-5
- Fix for CVE-2023-34241
* Wed May 24 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2.7-4
- Fix for CVE-2023-32324
* Fri Mar 24 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-3
- Fix CVE-2020-10001, CVE-2019-2228
* Mon Feb 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-2
- Fix CVE-2018-4300, CVE-2022-26691
* Mon Jun 20 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-1
- Build cups
