Summary:        The conntrack-tools are a set of userspace tools for Linux
Name:           conntrack-tools
Version:        1.4.6
Release:        2%{?dist}
License:        GPLv2
URL:            http://conntrack-tools.netfilter.org
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1    %{name}=731252dac79ad80f7c8d2ea4ce876d174fed0ebf
Source1:        conntrackd.service
Patch0:         conntrack-tools-compiling-support-libtirpc.patch
BuildRequires:  libnetfilter_conntrack-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  libmnl-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libnetfilter_cttimeout-devel
BuildRequires:  libnetfilter_cthelper-devel
BuildRequires:  libnetfilter_queue-devel
BuildRequires:  systemd-devel
Requires:       libmnl
Requires:       libnetfilter_conntrack
Requires:       libnfnetlink
Requires:       libnetfilter_cttimeout
Requires:       libnetfilter_cthelper
Requires:       libnetfilter_queue
Requires:       systemd
Provides:       conntrack

%description
The conntrack-tools are a set of free software userspace tools for Linux that allow system administrators interact with the Connection Tracking System, which is the module that provides stateful packet inspection for iptables. The conntrack-tools are the userspace daemon conntrackd and the command line interface conntrack.
The conntrack-tools package contains two programs:

  - conntrack:  the command line interface to interact with the connection
                tracking system.

  - conntrackd: the connection tracking userspace daemon that can be used to
                deploy highly available GNU/Linux firewalls and collect
                statistics of the firewall use.

%prep
%autosetup -p1

aclocal
autoconf

%build
%configure \
        --enable-systemd \
        --disable-static \
        --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'
install -vdm 755 %{buildroot}%{_sysconfdir}/conntrackd
install -m 0644 doc/stats/conntrackd.conf %{buildroot}%{_sysconfdir}/conntrackd
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/conntrackd.service
install -vdm 755 %{buildroot}%{_datadir}/conntrackd
install -vdm 755 %{buildroot}%{_sharedstatedir}/conntrackd

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post  conntrackd.service

%preun
/sbin/ldconfig
%systemd_preun conntrackd.service

%postun
/sbin/ldconfig
%systemd_postun conntrackd.service

%files
%defattr(-,root,root,-)
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%{_mandir}/man8/*
%{_mandir}/man5/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_datadir}/conntrackd
%{_sharedstatedir}/conntrackd

%changelog
*   Tue Oct 19 2021 Ankit Jain <ankitja@vmware.com> 1.4.6-2
-   Changing files/directory ownership to root
*   Mon Jan 25 2021 Gerrit Photon <photon-checkins@vmware.com> 1.4.6-1
-   Automatic Version Bump
*   Tue Dec 22 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.4.5-3
-   Bump version as a part of autospec library upgrade
*   Wed Sep 11 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.5-2
-   Add provides for conntrack
*   Fri Mar 01 2019 Ankit Jain <ankitja@vmware.com> 1.4.5-1
-   Initial build. First version
