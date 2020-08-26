Summary:        Connection tracking userspace tools for Linux.
Name:           conntrack-tools
Version:        1.4.6
Release:        1%{?dist}
License:        GPLv2
URL:            http://conntrack-tools.netfilter.org/
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 conntrack-tools=731252dac79ad80f7c8d2ea4ce876d174fed0ebf
Source1:        conntrackd.conf
Source2:        conntrackd.service
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires: gcc
BuildRequires: systemd-devel
BuildRequires: libtirpc-devel
BuildRequires: libmnl-devel
BuildRequires: libnfnetlink-devel
BuildRequires: libnetfilter_conntrack-devel
BuildRequires: libnetfilter_cttimeout-devel
BuildRequires: libnetfilter_cthelper-devel
BuildRequires: libnetfilter_queue-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: systemd
Requires:      systemd
Requires:      libmnl
Requires:      libnetfilter_conntrack
Requires:      libnetfilter_cthelper
Requires:      libnetfilter_cttimeout
Requires:      libnetfilter_queue
Requires:      libnfnetlink

%description
The conntrack-tools are a set of free software userspace tools for Linux that
allow system administrators interact with the Connection Tracking System,
which is the module that provides stateful packet inspection for iptables.

%prep
%setup -q

%build
autoreconf -fi
%configure --disable-static --enable-systemd
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/conntrackd/
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/

%files
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%dir %{_libdir}/conntrack-tools
%{_libdir}/conntrack-tools/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%post
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
%systemd_postun conntrackd.service

%changelog
*  Tue Aug 25 2020 Ashwin H <ashwinh@vmware.com> 1.4.6-1
-  Initial version
