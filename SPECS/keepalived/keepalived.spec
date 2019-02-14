Summary:    HA monitor built upon LVS, VRRP and services poller 
Name:       keepalived
Version:    1.3.5
Release:    2%{?dist}
License:    GPL
URL:        http://www.keepalived.org/
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:     http://www.keepalived.org/software/%{name}-%{version}.tar.gz
%define sha1 keepalived=5a373d8f5d382700cf53b827947a92a7f4cef148
Source1:     keepalived.service
Patch0:         CVE-2018-19044.patch 
BuildRequires:    openssl-devel
BuildRequires:    iptables
BuildRequires:    libmnl-devel
BuildRequires:    ipset-devel
BuildRequires:    libnl-devel
BuildRequires:    libnfnetlink-devel
BuildRequires:    net-snmp-devel
BuildRequires:    systemd
Requires:         systemd

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
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix}	\
    --bindir=%{_bindir}	\
    --libdir=%{_libdir}	\
    --sysconfdir=%{_sysconfdir} \
    --with-systemdsystemunitdir=%{_unitdir} \
    --enable-snmp       \
    --enable-snmp-rfc
make %{?_smp_mflags} STRIP=/bin/true

%install
make install DESTDIR=%{buildroot}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/keepalived.service
rm -rf %{buildroot}%{_sysconfdir}/keepalived/samples/*

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
%{_sbindir}/keepalived
%{_bindir}/genhash
%{_unitdir}/keepalived.service
%config(noreplace) %{_sysconfdir}/sysconfig/keepalived
%config(noreplace) %{_sysconfdir}/keepalived/keepalived.conf
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*

%changelog
*   Thu Feb 14 2019 <ashwinh@vmware.com> 1.3.5-2
-   Fix CVE-2018-19044
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.5-1
-   Initial build.  First version
