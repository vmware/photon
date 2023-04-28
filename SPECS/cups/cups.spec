Summary:        The Common UNIX Printing System
Name:           cups
Version:        2.2.7
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://openprinting.github.io/cups
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/OpenPrinting/cups/releases/download/v%{version}/cups-%{version}.tar.gz
%define sha512 %{name}=143f085ce0a8953d9ab277a46369dcf337bcdd84f5a4dc0ed5dba7a5d0188dc62825728d56e8baf4a2b4f96f2086b3798660016924969d69d28483809a031a4d
Patch0:         CVE-2018-4300.patch
Patch1:         CVE-2022-26691.patch
Patch2:         CVE-2020-10001.patch
Patch3:         CVE-2019-2228.patch

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

%changelog
* Fri Mar 24 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-3
- Fix CVE-2020-10001, CVE-2019-2228
* Mon Feb 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-2
- Fix CVE-2018-4300, CVE-2022-26691
* Mon Jun 20 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-1
- Build cups
