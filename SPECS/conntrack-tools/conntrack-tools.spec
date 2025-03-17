Summary:        Connection tracking userspace tools for Linux.
Name:           conntrack-tools
Version:        1.4.7
Release:        4%{?dist}
URL:            http://conntrack-tools.netfilter.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2

Source1:        conntrackd.conf

Source2:        conntrackd.service

Source3: license.txt
%include %{SOURCE3}

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

Requires:      systemd
Requires:      libmnl
Requires:      libnetfilter_conntrack
Requires:      libnetfilter_cthelper
Requires:      libnetfilter_cttimeout
Requires:      libnetfilter_queue
Requires:      libnfnetlink
Provides:      conntrack

%description
The conntrack-tools are a set of free software userspace tools for Linux that
allow system administrators interact with the Connection Tracking System,
which is the module that provides stateful packet inspection for iptables.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
    --disable-static \
    --enable-systemd

%make_build %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/conntrackd
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
/sbin/ldconfig
%systemd_postun conntrackd.service

%files
%defattr(-, root, root)
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.4.7-4
- Release bump for SRP compliance
* Fri Jun 14 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.7-3
- Fix conntrackd.service failure
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.7-2
- Bump version as a part of libtirpc upgrade
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com.com> 1.4.7-1
- Version bump
* Sun Oct 17 2021 Susant Sahani <ssahani@vmware.com.com> 1.4.6-3
- Rename conntrackd.conf eth2 -> eth0
* Sat Feb 27 2021 Andrew Williams <andy@tensixtyone.com> 1.4.6-2
- Add provide for conntrack
* Tue Aug 25 2020 Ashwin H <ashwinh@vmware.com> 1.4.6-1
- Initial version
