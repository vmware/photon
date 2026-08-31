%global build_if %{photon_subrelease} >= 91
%global kea_services kea-dhcp4.service kea-dhcp6.service kea-dhcp-ddns.service

Summary:      A modern, scalable, robust DHCPv4 and DHCPv6 server.
Name:         kea
Version:      3.1.9
Release:      5%{?dist}
Url:          https://www.isc.org/kea/
Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon

Source0: https://github.com/isc-projects/kea/archive/refs/tags/Kea-%{version}.tar.gz
Source1: %{name}.tmpfiles
Source2: %{name}.sysusers

Source3: license.txt
%include %{SOURCE3}

Source4: kea-dhcp4.service
Source5: kea-dhcp6.service
Source6: kea-dhcp-ddns.service
Source7: disable-kea-by-default.preset

Patch0: 0001-keactrl-Use-absolute-sysconfdir-and-localstatedir.patch

BuildRequires: meson
BuildRequires: log4cplus-devel
BuildRequires: boost-devel
BuildRequires: krb5-devel
BuildRequires: shadow
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros

Requires:      kea-libs = %{version}-%{release}
Requires:      systemd
Requires(pre): shadow
Requires(pre): systemd-rpm-macros
Obsoletes:     dhcp-server

%description
Kea provides DHCPv4 and DHCPv6 servers, a dynamic DNS update module,
a portable DHCP library, libdhcp++, a NETCONF agent that provides a
YANG/NETCONF interface for Kea, and a DHCP benchmarking tool, perfdhcp.
Kea is developed by Internet Systems Consortium, Inc.

%package  devel
Summary:  Development tools for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %name-devel package contains the libraries and header files
needed for development with %name.

%package  libs
Summary:  Libraries for %{name}
Group:    System Environment/Libraries

%description libs
This package contains minimal set of shared %{name} libraries.

%package  python3
Summary:  %{name} python3 lib
Group:    Development/Libraries
Requires: python3
Requires: %{name} = %{version}-%{release}

%description python3
This contains %{name} python3 libraries.

%package  docs
Summary:  %{name} docs
Group:    Development/Tools
Requires: %{name} = %{version}-%{release}

%description docs
The %name-docs contains %name package doc files.

%prep
%autosetup -p1 -n kea-Kea-%{version}

%build
%meson -Dpostgresql=disabled -Dnetconf=disabled -Dmysql=disabled
%meson_build

%install
%meson_install

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

install -vdm 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/kea-dhcp4.service
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/kea-dhcp6.service
install -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/kea-dhcp-ddns.service
install -p -D -m 0644 %{SOURCE7} %{buildroot}%{_presetdir}/50-%{name}.preset

%pre
%sysusers_create_compat %{SOURCE2}

%post
systemd-tmpfiles --create %{name}.conf
%systemd_post %{kea_services}

%preun
%systemd_preun %{kea_services}

%postun
%systemd_postun_with_restart %{kea_services}

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
# kea-shell is a python script, thus move it to -python3
%exclude %{_sbindir}/kea-shell
%{_datadir}/kea
%{_sysconfdir}/kea
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_unitdir}/kea-dhcp4.service
%{_unitdir}/kea-dhcp6.service
%{_unitdir}/kea-dhcp-ddns.service
%{_presetdir}/50-%{name}.preset
%dir %attr(0750,kea,kea) %{_sharedstatedir}/kea
%dir %attr(0750,kea,kea) %{_localstatedir}/log/kea

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files libs
%defattr(-,root,root)
%{_libdir}/kea
%{_libdir}/lib*.so.*

%files python3
%defattr(-,root,root)
%{python3_sitelib}/*
%{_sbindir}/kea-shell

%files docs
%defattr(-,root,root)
%{_docdir}/*

%changelog
* Mon Aug 31 2026 Daniel Casota <dcasota@gmail.com> 3.1.9-5
- Ship systemd units for kea-dhcp4, kea-dhcp6 and kea-dhcp-ddns
- Fix keactrl looking for its config under /usr/etc instead of /etc
- Ship a disable-by-default preset so the DHCP servers are not enabled on install
* Mon Jun 22 2026 Bo Gan <bo.gan@broadcom.com> 3.1.9-3
- Disable mysql support
* Mon Jun 15 2026 Bo Gan <bo.gan@broadcom.com> 3.1.9-2
- Regenerate license
* Wed Jun 03 2026 Bo Gan <bo.gan@broadcom.com> 3.1.9-1
- Initial packaging
