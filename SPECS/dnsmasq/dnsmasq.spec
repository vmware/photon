Summary:	DNS proxy with integrated DHCP server
Name:		dnsmasq
Version:	2.76
Release:	1%{?dist}
License:	GPLv2 or GPLv3
Group:		System Environment/Daemons
URL:		http://www.thekelleys.org.uk/dnsmasq/
Source:	        %{name}-%{version}.tar.xz
%define sha1 dnsmasq=db42d7297dc0a05d51588baa2f298ebb42fcef99
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	dnsmasq

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%prep
%setup -q

%build
make %{?_smp_mflags}

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

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

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
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/*
%dir %{_sharedstatedir}
%config  /usr/share/dnsmasq/trust-anchors.conf

%changelog
*   Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-1
-   Upgrade to 2.76 to address CVE-2015-8899
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.75-2
-   GA - Bump release of all rpms
*   Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> 2.75-1
-   Initial version
