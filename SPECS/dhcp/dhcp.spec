Summary:      Dynamic host configuration protocol
Name:         dhcp
Version:      4.4.3
Release:      5%{?dist}
Url:          http://isc.org/products/DHCP/
Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon

Source0:      ftp://ftp.isc.org/isc/dhcp/${version}/%{name}-%{version}.tar.gz
Source1:      dhclient-script
Source2:      dhclient.conf
Source3:      dhcp.service
Source4:      dhcrelay.service

Source5: license.txt
%include %{SOURCE5}

Patch0:       CVE-2022-2928.4-4-3.patch
Patch1:       CVE-2022-2929.4-4-3.patch

BuildRequires:  systemd-devel

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
%autosetup -p1

%build
autoreconf -vfi
export CFLAGS="-D_PATH_DHCLIENT_SCRIPT='\"/sbin/dhclient-script\"'  \
        -D_PATH_DHCPD_CONF='\"/etc/dhcp/dhcpd.conf\"'               \
        -D_PATH_DHCLIENT_CONF='\"/etc/dhcp/dhclient.conf\"'"        \

%configure \
   --with-srv-lease-file=%{_sharedstatedir}/dhcpd/dhcpd.leases \
   --with-srv6-lease-file=%{_sharedstatedir}/dhcpd/dhcpd6.leases \
   --with-cli-lease-file=%{_sharedstatedir}/dhclient/dhclient.leases \
   --with-cli6-lease-file=%{_sharedstatedir}/dhclient/dhclient6.leases \
   --with-srv-pid-file=%{_rundir}/dhcpd.pid \
   --with-srv6-pid-file=%{_rundir}/dhcpd6.pid \
   --with-cli-pid-file=%{_rundir}/dhclient.pid \
   --with-cli6-pid-file=%{_rundir}/dhclient6.pid \
   --with-relay-pid-file=%{_rundir}/dhcrelay.pid \
   --enable-log-pid \
   --enable-paranoia \
   --enable-early-chroot \
   --enable-binary-leases \
   --with-systemd

# make doesn't support _smp_mflags
make

%install
%make_install %{?_smp_mflags}

install -Dpm 0755 %{SOURCE1} %{buildroot}%{_sbindir}/dhclient-script

mkdir -p %{buildroot}%{_sysconfdir}/dhcp \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/dhcp \
         %{buildroot}%{_sharedstatedir}/{dhcpd,dhclient}

install -Dpm 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/dhcp/
install -Dpm 0755 %{SOURCE3} %{buildroot}%{_unitdir}/
install -Dpm 0755 %{SOURCE4} %{buildroot}%{_unitdir}/

install -vdm 755 %{buildroot}%{_sharedstatedir}/dhclient
install -vdm 755 %{buildroot}%{_sysconfdir}/default

cat > %{buildroot}%{_sysconfdir}/default/dhcpd << "EOF"
DHCPD_OPTS=
EOF

touch %{buildroot}%{_sysconfdir}/dhcp/{dhcpd.conf,dhcpd6.conf}
touch %{buildroot}%{_sharedstatedir}/dhcpd/{dhcpd.leases,dhcpd6.leases}

rm -f %{buildroot}%{_sysconfdir}/dhclient.conf.example \
      %{buildroot}%{_sysconfdir}/dhcpd.conf.example

install -vdm 755 %{buildroot}%{_sysconfdir}/dhcp/dhclient.d

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

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
%dir %{_sharedstatedir}/dhcpd
%config(noreplace) %{_sysconfdir}/default/dhcpd
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd.conf
%config(noreplace) %{_sysconfdir}/dhcp/dhcpd6.conf
%config(noreplace) %{_sharedstatedir}/dhcpd/dhcpd.leases
%config(noreplace) %{_sharedstatedir}/dhcpd/dhcpd6.leases

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
%{_unitdir}/dhcrelay.service

%files client
%defattr(-,root,root)
%dir %{_sysconfdir}/dhcp
%dir %{_sysconfdir}/dhcp/dhclient.d
%config(noreplace) %{_sysconfdir}/dhcp/dhclient.conf
%{_sbindir}/dhclient
%{_sbindir}/dhclient-script
%dir %{_sharedstatedir}/dhclient
%{_mandir}/man5/dhclient.conf.5.gz
%{_mandir}/man5/dhclient.leases.5.gz
%{_mandir}/man8/dhclient-script.8.gz
%{_mandir}/man8/dhclient.8.gz

%changelog
* Tue Feb 25 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.4.3-5
- Fix license
* Thu Feb 13 2025 Tapas Kundu <tapas.kundu@broadcom.com> 4.4.3-4
- Include /etc/dhcp/dhclient.d directory as part of dhcp-client
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.4.3-3
- Release bump for SRP compliance
* Mon Sep 25 2023 Harinadh D <hdommaraju@vmware.com> 4.4.3-2
- Fix CVE-2022-2928,CVE-2022-2929
* Tue Aug 30 2022 Susant Sahani <ssahani@vmware.com> 4.4.3-1
- Version bump
* Tue Nov 02 2021 Susant Sahani <ssahani@vmware.com> 4.4.2-5
- Add unit file dhcrelay.service
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
