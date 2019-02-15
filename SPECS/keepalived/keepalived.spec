Summary:        HA monitor built upon LVS, VRRP and services poller
Name:           keepalived
Version:        2.0.10
Release:        1%{?dist}
License:        GPL
URL:            http://www.keepalived.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/acassen/keepalived/archive/keepalived-v%{version}.zip
%define sha1    %{name}-v%{version}=86b4307f7827c42fcce1fdb270ff614b569741cd
Source1:        %{name}.service
BuildRequires:  openssl-devel
BuildRequires:  iptables-devel
BuildRequires:  libmnl-devel
BuildRequires:  ipset-devel
BuildRequires:  libnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  net-snmp-devel
BuildRequires:  systemd
BuildRequires:  unzip
Requires:       systemd
Requires:       libnl-devel

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
%setup -q

%build
autoreconf -f -i
%configure \
    --with-systemdsystemunitdir=%{_unitdir} \
    --enable-snmp       \
    --enable-snmp-rfc
make %{?_smp_mflags} STRIP=/bin/true

%install
make install DESTDIR=%{buildroot}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
rm -rf %{buildroot}%{_sysconfdir}/%{name}/samples/*

%check
# A build could silently have LVS support disabled if the kernel includes can't
# be properly found, we need to avoid that.
if ! grep -q "#define _WITH_LVS_ *1" lib/config.h; then
    %{__echo} "ERROR: We do not want keepalived lacking LVS support."
    exit 1
fi

%post
/sbin/ldconfig
%systemd_post keepalived.service

%preun
%systemd_preun keepalived.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart keepalived.service

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}/README
%{_sbindir}/%{name}
%{_bindir}/genhash
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*

%changelog
*   Fri Feb 15 2019 Ashwin H <ashwinh@vmware.com> 2.0.10-1
-   Updated to version 2.0.10
*   Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 2.0.7-1
-   Updated to version 2.0.7
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.3.5-2
-   Add iptables-devel to BuildRequires
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.5-1
-   Initial build.  First version
