Summary:	DNS proxy with integrated DHCP server
Name:		dnsmasq
Version:	2.75
Release:	2%{?dist}
License:	GPLv2 or GPLv3
Group:		System Environment/Daemons
URL:		http://www.thekelleys.org.uk/dnsmasq/
Source:		%{name}-%{version}.tar.xz
%define sha1 dnsmasq=e3312377f2ce75ebae1408fee41414a6fc03458f
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	dnsmasq

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%prep
%setup -q

%build
make %{?_smp_mflags} 
make -C contrib/wrt %{?_smp_mflags} 

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

install -m 755 contrib/wrt/dhcp_release   %{buildroot}%{_bindir}/dhcp_release
install -m 644 contrib/wrt/dhcp_release.1 %{buildroot}%{_mandir}/man1/dhcp_release.1
install -m 755 contrib/wrt/dhcp_lease_time %{buildroot}%{_bindir}/dhcp_lease_time
install -m 644 contrib/wrt/dhcp_lease_time.1 %{buildroot}%{_mandir}/man1/dhcp_lease_time.1

mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/dnsmasq.service
[Unit]
Description=A lightweight, caching DNS proxy
After=network.target

[Service]
ExecStart=/usr/sbin/dnsmasq -k

[Install]
WantedBy=multi-user.target
EOF

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/systemd/*
%exclude %{_libdir}/debug
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/*
%dir %{_sharedstatedir}
%config  /usr/share/dnsmasq/trust-anchors.conf

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.75-2
-	GA - Bump release of all rpms
*       Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> 2.75-1
-       Initial version
