%global build_if %{photon_subrelease} <= 91

Summary:        The Common UNIX Printing System
Name:           cups
Version:        2.4.14
Release:        1.1%{?dist}
URL:            https://openprinting.github.io/cups
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/OpenPrinting/cups/releases/download/v%{version}/cups-%{version}-source.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Fix CVE-2025-61915
Patch1:  0001-Fix-various-issues-in-cupsd.patch

# Fix CVE-2025-58436
Patch2: 0001-Fix-unresponsive-cupsd-process-caused-by-a-slow-client.patch

BuildRequires:  automake
BuildRequires:  dbus-devel
BuildRequires:  pkg-config
BuildRequires:  Linux-PAM-devel
BuildRequires:  shadow
BuildRequires:  krb5-devel
BuildRequires:  libusb-devel
BuildRequires:  openssl-devel

Requires:       libusb
Requires:       dbus
Requires:       gnutls
Requires:       krb5
Requires:       zlib
Requires:       Linux-PAM
Requires:       shadow

%description
The Common Unix Printing System (CUPS) is a print spooler and associated utilities.
It is based on the "Internet Printing Protocol" and provides printing services to most PostScript and raster printers.

%package        devel
Summary:        Header and development files
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
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/pam.d/cups
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
* Wed Feb 11 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.4.14-1.1
- Bump after moving to SPECS/91
* Tue Nov 25 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.4.14-1
- Update to 2.4.14 and fix CVE-2025-61915 and CVE-2025-58436
* Sun Oct 19 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.4.11-4
- Fix build requires and packaging for a future package-builder change
- When shadow is present in build env, pam.d/cups is also packaged
* Thu Sep 11 2025 Ajay Kaher <ajay.kaher@broadcom.com> 2.4.11-3
- fix CVE-2025-58060
* Tue Jul 01 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.4.11-2
- Bump release to rescan licenses
* Mon Dec 16 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.4.11-1
- Update to v2.4.11 to fix CVEs
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.4.7-4
- Release bump for SRP compliance
* Thu Jun 06 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.4.7-3
- Fix CVE-2024-35235
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.7-2
- Bump version as a part of gnutls upgrade
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
