Summary:        The Common UNIX Printing System
Name:           cups
Version:        2.4.2
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://openprinting.github.io/cups
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/OpenPrinting/cups/releases/download/v%{version}/cups-%{version}.tar.gz
%define sha512  %{name}=1942a677a78df0dcfaaae4b93cf7bf4ba59865d270d89d893831cb47a02f6b7e581c56bbb9264d39504b46d81c3b17ba89f7c5e21f20628f12ddf7161ac6a574

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
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.2-3
- Bump version as a part of zlib upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.4.2-2
- Bump version as a part of krb5 upgrade
* Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.2-1
- Automatic Version Bump
* Mon Jun 20 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.7-1
- Build cups
