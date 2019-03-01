Summary:        The conntrack-tools are a set of userspace tools for Linux
Name:           conntrack-tools
Version:        1.4.5
Release:        1%{?dist}
License:        GPLv2
URL:            http://conntrack-tools.netfilter.org
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1    %{name}=7d03a8d6d9ef56a9980ebfe25a282123807f8dcb
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

%description
The conntrack-tools are a set of free software userspace tools for Linux that allow system administrators interact with the Connection Tracking System, which is the module that provides stateful packet inspection for iptables. The conntrack-tools are the userspace daemon conntrackd and the command line interface conntrack.
The conntrack-tools package contains two programs:

  - conntrack:  the command line interface to interact with the connection
                tracking system.

  - conntrackd: the connection tracking userspace daemon that can be used to
                deploy highly available GNU/Linux firewalls and collect
                statistics of the firewall use.

%prep
%setup -q
%patch0 -p1

aclocal
autoconf

%build
%configure \
        --enable-systemd \
        --disable-static \
        --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'
install -vdm 755 %{buildroot}%{_sysconfdir}/conntrackd
install -m 0644 doc/stats/conntrackd.conf %{buildroot}%{_sysconfdir}/conntrackd
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/conntrackd.service
install -vdm 755 %{buildroot}%{_datadir}/conntrackd
install -vdm 755 %{buildroot}%{_sharedstatedir}/conntrackd

%check
make %{?_smp_mflags} check

%pre -p /bin/sh
if ! getent group conntrackd >/dev/null; then
    groupadd -r conntrackd
fi
if ! getent passwd conntrackd >/dev/null; then
    useradd -r -g conntrackd -d /var/lib/conntrackd -s /sbin/nologin  -c "Conntrack tools User" conntrackd
fi
exit 0


%post
/sbin/ldconfig
chown -R conntrackd:conntrackd /var/lib/conntrackd
chown -R conntrackd:conntrackd /usr/share/conntrackd
%systemd_post  conntrackd.service

%preun
/sbin/ldconfig
%systemd_preun conntrackd.service

%postun -p /bin/sh
%systemd_postun_with_restart conntrackd.service
if [ $1 -eq 0 ] ; then
   getent passwd conntrackd > /dev/null
   if [ "$?" == "0" ] ; then
      userdel conntrackd
   fi
   getent group conntrackd >/dev/null
   if [ "$?" == "0" ] ; then
      groupdel conntrackd
   fi
fi
exit

%files
%defattr(-,conntrackd,conntrackd)
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_libdir}/%{name}/*.so
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_datadir}/conntrackd
%{_sharedstatedir}/conntrackd

%changelog
*   Fri Mar 01 2019 Ankit Jain <ankitja@vmware.com> 1.4.5-1
-   Initial build. First version

