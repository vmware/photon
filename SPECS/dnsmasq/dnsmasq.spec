%global _default_patch_fuzz 1
Summary:        DNS proxy with integrated DHCP server
Name:           dnsmasq
Version:        2.90
Release:        2%{?dist}
Group:          System Environment/Daemons
URL:            https://thekelleys.org.uk/dnsmasq/doc.html
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.xz
%define sha512 %{name}=e169de1892f935e219b0f49d90107f95cba42b40bca20bd3c973313c2cd4df58b929af6628cd988419051d81c3b4ccf8e9f816274df7d0840e79f5bf49602442

Source1: license.txt
%include %{SOURCE1}

Patch0:         enable_dnssec.patch

BuildRequires:  nettle-devel
BuildRequires:  systemd-rpm-macros

Requires:       systemd
Requires:       nettle

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%package        utils
Summary:        Utilities for changing DHCP server leases

%description    utils
Utilities that use DHCP protocol to query and remove a DHCP server's leases

%prep
%autosetup -p1

%build
%make_build
%make_build -C contrib/lease-tools

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/{man1,man8} \
         %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_sysconfdir}/%{name}.d \
         %{buildroot}%{_sysconfdir}/dbus-1/system.d

install src/%{name} %{buildroot}%{_sbindir}/%{name}
install %{name}.conf.example %{buildroot}%{_sysconfdir}/%{name}.conf
install dbus/%{name}.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/%{name}.8 %{buildroot}%{_mandir}/man8/
install -D trust-anchors.conf %{buildroot}%{_datadir}/%{name}/trust-anchors.conf

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

mkdir -p %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=A lightweight, caching DNS proxy
After=network.target

[Service]
ExecStart=%{_sbindir}/%{name} -k
Restart=always

[Install]
WantedBy=multi-user.target
EOF

#dnsmasq-utils subpackage
install -m 755 contrib/lease-tools/dhcp_release %{buildroot}%{_bindir}/dhcp_release
install -m 644 contrib/lease-tools/dhcp_release.1 %{buildroot}%{_mandir}/man1/dhcp_release.1
install -m 755 contrib/lease-tools/dhcp_release6 %{buildroot}%{_bindir}/dhcp_release6
install -m 644 contrib/lease-tools/dhcp_release6.1 %{buildroot}%{_mandir}/man1/dhcp_release6.1
install -m 755 contrib/lease-tools/dhcp_lease_time %{buildroot}%{_bindir}/dhcp_lease_time
install -m 644 contrib/lease-tools/dhcp_lease_time.1 %{buildroot}%{_mandir}/man1/dhcp_lease_time.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_unitdir}/*
%exclude %dir %{_libdir}/debug
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%dir %{_sharedstatedir}
%config %{_datadir}/%{name}/trust-anchors.conf

%files utils
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.90-2
- Release bump for SRP compliance
* Tue Feb 20 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 2.90-1
- Update to v2.90 to fix CVE-2023-50868, CVE-2023-50387
* Mon May 22 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.89-1
- Version bump
* Wed Dec 07 2022 Susant Sahai <ssahani@vmware.com> 2.88-1
- Version bump
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.87-1
- Automatic Version Bump
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.86-3
- Bump version as a part of nettle upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.86-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.86-1
- Automatic Version Bump
* Mon Aug 30 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.85-3
- Spec improvements
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.85-2
- Bump version as a part of nettle upgrade
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.85-1
- Automatic Version Bump
* Thu Feb 04 2021 Ankit Jain <ankitja@vmware.com> 2.84-1
- Update to 2.84
* Sat Jan 09 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.82-3
- Fix CVE-2020-25681,CVE-2020-25682,CVE-2020-25683,CVE-2020-25684
- CVE-2020-25685,CVE-2020-25686,CVE-2020-25687
* Mon Aug 24 2020 Ashwin H <ashwinh@vmware.com> 2.82-2
- Enable dnssec
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.82-1
- Automatic Version Bump to version 2.82
* Mon May 04 2020 Dweep Advani <dadvani@vmware.com> 2.79-3
- Preserve configuration files during package upgrades
* Thu Mar 05 2020 Ashwin H <ashwinh@vmware.com> 2.79-2
- Fix CVE-2019-14834. Add utils package
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.79-1
- Upgrading to version 2.79
* Tue Feb 13 2018 Xiaolin Li <xiaolinl@vmware.com> 2.76-5
- Fix CVE-2017-15107
* Mon Nov 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-4
- Always restart dnsmasq service on exit
* Wed Oct 11 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-3
- Fix CVE-2017-13704
* Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-2
- Fix CVE-2017-14491..CVE-2017-14496
* Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-1
- Upgrade to 2.76 to address CVE-2015-8899
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.75-2
- GA - Bump release of all rpms
* Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> 2.75-1
- Initial version
