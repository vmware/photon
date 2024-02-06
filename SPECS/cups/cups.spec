Summary:        The Common UNIX Printing System
Name:           cups
Version:        2.4.7
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://openprinting.github.io/cups
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/OpenPrinting/cups/releases/download/v%{version}/cups-%{version}.tar.gz
%define sha512  %{name}=27ca505a2868aa7bc248bac892aafe2a837633e73b6059d3ab4812264e3b0e786ef075751e8cc4300ce6bc43ef095e3d77dd3fce88ce8e72ca69b65093427bca

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

%package        devel
Summary:        Header and development files
License:        LGPLv2
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the header files to create applications

%prep
%autosetup -p1

%build
%configure \
        CFLAGS="%{optflags}" \
        CXXFLAGS="%{optflags}"

%make_build

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
%config %{_sysconfdir}/dbus-1/system.d/cups.conf
%{_unitdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libcups*.so.*
%dir %{_libdir}/cups
%{_libdir}/cups/*

%doc %{_mandir}/*
%doc %{_docdir}/cups
%{_datadir}/cups/
%{_datadir}/locale/

%files devel
%defattr(-,root,root)
%{_includedir}/cups/
%{_libdir}/libcups*.so
%{_libdir}/pkgconfig/cups.pc

%changelog
* Wed Feb 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.4.7-4
- Bump version as a part of dbus upgrade
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.7-3
- Bump version as a part of gnutls upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.7-2
- Bump version as a part of openssl upgrade
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 2.4.7-1
- Update to v2.4.7 to fix CVE-2023-4504
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 2.4.6-2
- Bump version as a part of krb5 upgrade
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.6-1
- Update to v2.4.6
* Thu Jun 15 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.2-5
- Fix for CVE-2023-34241
* Wed May 24 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.2-4
- Fix for CVE-2023-32324
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.2-3
- Bump version as a part of zlib upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.2-2
- Bump version as a part of krb5 upgrade
* Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.2-1
- Automatic Version Bump
* Mon Jun 20 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-1
- Build cups
