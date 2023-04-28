Summary:        DNS proxy with integrated DHCP server
Name:           dnsmasq
Version:        2.85
Release:        4%{?dist}
License:        GPLv2 or GPLv3
Group:          System Environment/Daemons
URL:            https://thekelleys.org.uk/dnsmasq/doc.html
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.xz
%define sha512  %{name}=8beefe76b46f7d561f40d0900ba68b260a199cb62ab5b653746e3a1104c04fb8899b9e7a160a1be4fe8782bfb1607b556e9ffb9c25c4e99653e4bc74fcc03b09

Patch0:         enable_dnssec.patch
Patch1:         CVE-2022-0934.patch
Patch2:         CVE-2023-28450.patch
BuildRequires:  systemd
BuildRequires:  nettle-devel

Requires:       nettle
Requires:       systemd

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%package        utils
Summary:        Utilities for changing DHCP server leases

%description    utils
Utilities that use DHCP protocol to query and remove a DHCP server's leases

%prep
%autosetup -p1

%build
make %{?_smp_mflags}
make -C contrib/lease-tools %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/{man1,man8} \
         %{buildroot}%{_sharedstatedir}/dnsmasq \
         %{buildroot}%{_sysconfdir}/dnsmasq.d \
         %{buildroot}%{_sysconfdir}/dbus-1/system.d \
         %{buildroot}%{_unitdir}

install src/%{name} %{buildroot}%{_sbindir}/%{name}
install dnsmasq.conf.example %{buildroot}%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 %{buildroot}%{_mandir}/man8/
install -D trust-anchors.conf %{buildroot}%{_datadir}/%{name}/trust-anchors.conf

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

cat << EOF >> %{buildroot}%{_unitdir}/dnsmasq.service
[Unit]
Description=A lightweight, caching DNS proxy
After=network.target

[Service]
ExecStart=/usr/sbin/dnsmasq -k
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

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_unitdir}/*
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/dnsmasq.d
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dnsmasq.conf
%dir %{_sharedstatedir}
%config %{_datadir}/%{name}/trust-anchors.conf
%exclude %dir %{_libdir}/debug

%files utils
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Apr 03 2023 Anmol Jain <anmolja@vmware.com> 2.85-4
- Fix for CVE-2023-28450
* Thu Mar 09 2023 Srish Srinivasan <ssrish@vmware.com> 2.85-3
- fixed CVE-2022-0934
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.85-2
- Exclude debug symbols properly
* Mon Aug 30 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.85-1
- Upgrade version to 2.85 to fix CVE-2021-3448
* Sat Apr 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.82-2
- Bump version as a part of nettle upgrade
* Sat Jan 09 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.82-1
- Fix CVE-2020-25681,CVE-2020-25682,CVE-2020-25683,CVE-2020-25684
- CVE-2020-25685,CVE-2020-25686,CVE-2020-25687
* Mon Aug 24 2020 Ashwin H <ashwinh@vmware.com> 2.79-5
- Enable dnssec
* Mon May 04 2020 Dweep Advani <dadvani@vmware.com> 2.79-4
- Preserve configuration files during package upgrades
* Mon Jan 13 2020 <ashwinh@vmware.com> 2.79-3
- Fix CVE-2019-14834
* Tue Mar 26 2019 <ashwinh@vmware.com> 2.79-2
- Add dnsmasq-utils sub-package
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
