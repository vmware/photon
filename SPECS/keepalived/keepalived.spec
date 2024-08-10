Summary:        HA monitor built upon LVS, VRRP and services poller
Name:           keepalived
Version:        2.2.7
Release:        2%{?dist}
License:        GPL
URL:            http://www.keepalived.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/acassen/keepalived/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=617ea91a8fcf9cabb4a5c92e9131ed3efc40930e823c77359ec0c7e82bae3f899108443afbb214678437caac1b649a710fa5f783d370fd3030ae9319be522623

Source1: %{name}.service
# Backport of Upstream PR: https://github.com/acassen/keepalived/pull/2448/commits
# to fix CVE-2024-41184
Patch0: 0001-lib-don-t-return-subtracted-addresses-for-rb_find-co.patch
Patch1: 0002-vrrp-Handle-empty-ipset-names-with-vrrp_ipsets-keywo.patch
Patch2: 0003-vrrp-handle-empty-iptables-chain-names-vrrp_iptables.patch
Patch3: 0004-vrrp-and-ipvs-handle-empty-nftables-chain-names.patch
Patch4: 0005-configure-add-enable-sanitize-address-option.patch

BuildRequires:  openssl-devel
BuildRequires:  iptables-devel
BuildRequires:  libmnl-devel
BuildRequires:  ipset-devel
BuildRequires:  libnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  net-snmp-devel
BuildRequires:  systemd-devel
BuildRequires:  unzip

Requires:       systemd
Requires:       libnl
Requires:       net-snmp
Requires:       openssl
Requires:       iptables

%description
The main goal of the keepalived project is to add a strong & robust keepalive
facility to the Linux Virtual Server project. This project is written in C with
multilayer TCP/IP stack checks. Keepalived implements a framework based on
three family checks : Layer3, Layer4 & Layer5/7. This framework gives the
daemon the ability to check the state of an LVS server pool. When one of the
servers of the LVS server pool is down, keepalived informs the linux kernel via
a setsockopt call to remove this server entry from the LVS topology. In
addition keepalived implements an independent VRRPv2 stack to handle director
failover. So in short keepalived is a userspace daemon for LVS cluster nodes
healthchecks and LVS directors failover.

%prep
%autosetup -p1

%build
autoreconf -f -i
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --enable-snmp       \
    --enable-snmp-rfc

%make_build STRIP=/bin/true

%install
%make_install %{?_smp_mflags}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
rm -rf %{buildroot}%{_sysconfdir}/%{name}/samples/*

%if 0%{?with_check}
%check
# A build could silently have LVS support deactivated if the kernel includes can't
# be properly found, we need to avoid that.
if ! grep -q "#define _WITH_LVS_ *1" lib/config.h; then
  echo "ERROR: We do not want keepalived lacking LVS support."
  exit 1
fi
%endif

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}/README
%{_sbindir}/%{name}
%{_bindir}/genhash
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/%{name}/%{name}.conf.sample
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*

%changelog
* Fri Aug 09 2024 Ankit Jain <sshedi@vmware.com> 2.2.7-2
- Fix for CVE-2024-41184
* Tue May 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2.7-1
- Upgrade to v2.2.7
* Mon Jan 23 2023 Ankit Jain <ankitja@vmware.com> 2.1.5-5
- Fix CVE-2021-44225
* Fri Sep 17 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.5-4
- Bump up release for openssl
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 2.1.5-3
- Replacement of ITS suggested words.
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.5-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.5-1
- Automatic Version Bump
* Thu Jun 25 2020 Ajay Kaher <akaher@vmware.com> 2.1.3-2
- Corrected sha1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.3-1
- Automatic Version Bump
* Fri Feb 15 2019 Ashwin H <ashwinh@vmware.com> 2.0.10-1
- Updated to version 2.0.10
* Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 2.0.7-1
- Updated to version 2.0.7
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.3.5-2
- Add iptables-devel to BuildRequires
* Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.5-1
- Initial build.  First version
