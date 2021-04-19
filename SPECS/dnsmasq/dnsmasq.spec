Summary:        DNS proxy with integrated DHCP server
Name:           dnsmasq
Version:        2.84
Release:        2%{?dist}
License:        GPLv2 or GPLv3
Group:          System Environment/Daemons
URL:            http://www.thekelleys.org.uk/dnsmasq/
Source:         %{name}-%{version}.tar.xz
%define sha1    dnsmasq=60f6b8a6a86987613247c8dc32f61e28599ae285
Patch0:         enable_dnssec.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  nettle-devel
Requires:       nettle

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%package        utils
Summary:        Utilities for changing DHCP server leases

%description    utils
Utilities that use DHCP protocol to query and remove a DHCP server's leases

%prep
%autosetup

%build
make %{?_smp_mflags}
make -C contrib/lease-tools %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sharedstatedir}/dnsmasq
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_bindir}
install src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
install dnsmasq.conf.example %{buildroot}%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 %{buildroot}%{_mandir}/man8/
install -D trust-anchors.conf %{buildroot}%{_datadir}/%{name}/trust-anchors.conf

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/dnsmasq.service
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
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
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
%{_libdir}/systemd/*
%exclude %{_libdir}/debug
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/dnsmasq.d
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dnsmasq.conf
%dir %{_sharedstatedir}
%config  /usr/share/dnsmasq/trust-anchors.conf

%files utils
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Mon Apr 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.84-2
-   Bump version as a part of nettle upgrade
*   Thu Feb 04 2021 Ankit Jain <ankitja@vmware.com> 2.84-1
-   Update to 2.84
*   Sat Jan 09 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.82-3
-   Fix CVE-2020-25681,CVE-2020-25682,CVE-2020-25683,CVE-2020-25684
-   CVE-2020-25685,CVE-2020-25686,CVE-2020-25687
*   Mon Aug 24 2020 Ashwin H <ashwinh@vmware.com> 2.82-2
-   Enable dnssec
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.82-1
-   Automatic Version Bump to version 2.82
*   Mon May 04 2020 Dweep Advani <dadvani@vmware.com> 2.79-3
-   Preserve configuration files during package upgrades
*   Thu Mar 05 2020 Ashwin H <ashwinh@vmware.com> 2.79-2
-   Fix CVE-2019-14834. Add utils package
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 2.79-1
-   Upgrading to version 2.79
*   Tue Feb 13 2018 Xiaolin Li <xiaolinl@vmware.com> 2.76-5
-   Fix CVE-2017-15107
*   Mon Nov 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-4
-   Always restart dnsmasq service on exit
*   Wed Oct 11 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-3
-   Fix CVE-2017-13704
*   Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-2
-   Fix CVE-2017-14491..CVE-2017-14496
*   Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-1
-   Upgrade to 2.76 to address CVE-2015-8899
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.75-2
-   GA - Bump release of all rpms
*   Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> 2.75-1
-   Initial version
