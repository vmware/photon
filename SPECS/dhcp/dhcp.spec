Summary:      Dynamic host configuration protocol
Name:         dhcp
Version:      4.4.2
Release:      4%{?dist}
License:      ISC
Url:          http://isc.org/products/DHCP/
Source0:      ftp://ftp.isc.org/isc/dhcp/${version}/%{name}-%{version}.tar.gz
%define sha1  dhcp=cb4ba6617e1bc2e3cbf770be5c0443b1ad276db5
Source1:      dhclient-script
Source2:      dhclient.conf
Source3:      dhcp.service

Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon

Patch0:       dhcp-nowplusinterval.patch
Patch1:       dhcp-4.4.2-fno-common.patch
Patch2:       dhcp-CVE-2021-25217.patch

BuildRequires:  systemd

%description
The ISC DHCP package contains both the client and server programs for DHCP.
dhclient (the client) is used for connecting to a network which uses DHCP to
assign network addresses. dhcpd (the server) is used for assigning network
addresses on private networks.

%package libs
Summary:    Libraries for dhcp
%description libs
Libraries for the dhcp.

%package devel
Summary:    Development Libraries and header files for dhcp
Requires:   dhcp-libs
%description devel
Headers and libraries for the dhcp.

%package server
Summary:    Provides the ISC DHCP server
Requires:   dhcp-libs
%description server
dhcpd is the name of a program that operates as a daemon on a server to
provide Dynamic Host Configuration Protocol (DHCP) service to a network.
Clients may solicit an IP address (IP) from a DHCP server when they need one

%package client
Summary:    Provides the ISC DHCP client daemon and dhclient-script
Requires:   dhcp-libs
Requires:   ipcalc
Requires:   iputils
%description client

The ISC DHCP Client, dhclient, provides a means for configuring one or
more network interfaces using the Dynamic Host Configuration Protocol,
BOOTP protocol, or if these protocols fail, by statically assigning an address.

%prep
%autosetup -p1 %{name}-%{version}

%build
autoreconf --verbose --force --install
export CFLAGS="-D_PATH_DHCLIENT_SCRIPT='\"/sbin/dhclient-script\"'  \
        -D_PATH_DHCPD_CONF='\"/etc/dhcp/dhcpd.conf\"'               \
        -D_PATH_DHCLIENT_CONF='\"/etc/dhcp/dhclient.conf\"'"        \

%configure \
       --with-srv-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd.leases \
       --with-srv6-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd6.leases \
       --with-cli-lease-file=%{_localstatedir}/lib/dhclient/dhclient.leases \
       --with-cli6-lease-file=%{_localstatedir}/lib/dhclient/dhclient6.leases \
       --with-srv-pid-file=%{_localstatedir}/run/dhcpd.pid \
       --with-srv6-pid-file=%{_localstatedir}/run/dhcpd6.pid \
       --with-cli-pid-file=%{_localstatedir}/run/dhclient.pid \
       --with-cli6-pid-file=%{_localstatedir}/run/dhclient6.pid \
       --with-relay-pid-file=%{_localstatedir}/run/dhcrelay.pid \
       --enable-log-pid \
       --enable-paranoia \
       --enable-early-chroot \
       --enable-binary-leases \
       --with-systemd

# make doesn't support _smp_mflags
make -j1

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}/dhclient-script

mkdir -p %{buildroot}/%{_sysconfdir}/dhcp
install -D -p -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/dhcp/

mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0755 %{SOURCE3} %{buildroot}%{_unitdir}/

install -v -dm 755 %{buildroot}%{_localstatedir}/lib/dhclient
install -v -dm 755 %{buildroot}%{_sysconfdir}/default

cat > %{buildroot}%{_sysconfdir}/default/dhcpd << "EOF"
DHCPD_OPTS=
EOF

mkdir -p %{buildroot}%{_sysconfdir}/dhcp
touch %{buildroot}%{_sysconfdir}/dhcp/dhcpd.conf
touch %{buildroot}%{_sysconfdir}/dhcp/dhcpd6.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/dhcpd/
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd.leases
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd6.leases
mkdir -p %{buildroot}%{_localstatedir}/lib/dhclient/

rm -f %{buildroot}%{_sysconfdir}/dhclient.conf.example
rm -f %{buildroot}%{_sysconfdir}/dhcpd.conf.example

#%check
#Commented out %check due to missing support of ATF.

%ldconfig_scriptlets

%files libs
%defattr(-,root,root)
%{_libdir}/libdhcpctl.a
%{_libdir}/libomapi.a
%{_libdir}/libdhcp.a

%files devel
%defattr(-,root,root)
%{_includedir}/dhcpctl/dhcpctl.h
%{_includedir}/omapip/*.h

%files server
%defattr(-,root,root)
%dir %{_sysconfdir}/dhcp
%dir %{_localstatedir}/lib/dhcpd
%config(noreplace) %{_sysconfdir}/default/dhcpd
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd.conf
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd6.conf
%config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd.leases
%config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases

%{_bindir}/omshell
%{_sbindir}/dhcpd
%{_sbindir}/dhcrelay
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/dhcp-eval.5.gz
%{_mandir}/man5/dhcp-options.5.gz
%{_mandir}/man5/dhcpd.conf.5.gz
%{_mandir}/man5/dhcpd.leases.5.gz
%{_mandir}/man8/dhcpd.8.gz
%{_mandir}/man8/dhcrelay.8.gz
%{_unitdir}/dhcp.service

%files client
%defattr(-,root,root)
%dir %{_sysconfdir}/dhcp
%config(noreplace) %{_sysconfdir}/dhcp/dhclient.conf
%{_sbindir}/dhclient
%{_sbindir}/dhclient-script
%dir %{_localstatedir}/lib/dhclient
%{_mandir}/man5/dhclient.conf.5.gz
%{_mandir}/man5/dhclient.leases.5.gz
%{_mandir}/man8/dhclient-script.8.gz
%{_mandir}/man8/dhclient.8.gz

%changelog
* Tue Aug 24 2021 Susant Sahani <ssahani@vmware.com> 4.4.2-4
- Fix dhclient script
* Tue May 25 2021 Dweep Advani <dadvani@vmware.com> 4.4.2-3
- Patched for CVE-2021-25217
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 4.4.2-2
- GCC-10 support.
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 4.4.2-1
- Automatic Version Bump
* Thu Sep 19 2019 Keerthana K <keerthanak@vmware.com> 4.3.5-5
- Fix dhcpd fails with "Unable to set up timer: out of range"
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 4.3.5-4
- Commented out %check due to missing support of ATF.
* Thu Apr 20 2017 Divya Thaluru <dthaluru@vmware.com> 4.3.5-3
- Added default dhcp configuration and lease files
* Wed Dec 7 2016 Divya Thaluru <dthaluru@vmware.com> 4.3.5-2
- Added configuration file for dhcp service
* Mon Nov 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.3.5-1
- Upgraded to version 4.3.5.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.3.3-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.3.3-3
- GA - Bump release of all rpms
* Wed Mar 30 2016 Anish Swaminathan <anishs@vmware.com>  4.3.3-2
- Add patch for CVE-2016-2774
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
- Updated to version 4.3.3
* Wed Jul 15 2015 Divya Thaluru <dthaluru@vmware.com> 4.3.2-1
- Initial build.
