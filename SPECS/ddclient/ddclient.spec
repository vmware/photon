Name:           ddclient
Version:        3.8.3
Release:        2%{?dist}
Url:            https://sourceforge.net/p/ddclient/wiki/Home/
Summary:        Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider
License:        GPLv2
Group:          Applications
Source0:        http://downloads.sourceforge.net/project/ddclient/ddclient/ddclient-3.8.3.tar.bz2
%define sha1 ddclient=8668d8828a74ef4e7bca90890d7bbe414c37c3ff

Requires:       perl
Requires:       perl-IO-Socket-SSL
Requires:       perl-JSON-Any

BuildArch:      x86_64

%description
DDclient is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider. It was originally written by Paul Burry and is now mostly by wimpunk. It has the capability to update more than just dyndns and it can fetch your WAN-ipaddress in a few different ways.

%prep
%setup -q -n %{name}-%{version}

%install

install -vdm755 %{buildroot}/usr/sbin
cp ddclient %{buildroot}/usr/sbin/

install -vdm755 %{buildroot}/etc/ddclient
install -vdm755 %{buildroot}/var/cache/ddclient
install -vdm755 %{buildroot}/usr/lib/systemd/system

cp sample-etc_ddclient.conf %{buildroot}/etc/ddclient/ddclient.conf

cat << EOF >> %{buildroot}/usr/lib/systemd/system/ddclient.service
[Unit]
Description=Dynamic DNS Update Client
After=network.target
PartOf=network-online.target

[Service]
Type=forking
PIDFile=/var/run/ddclient.pid
ExecStart=/usr/sbin/ddclient

[Install]
WantedBy=network-online.target
EOF

%files
%defattr(-,root,root)
%{_sysconfdir}/ddclient/ddclient.conf
%{_sbindir}/ddclient
%{_lib}/systemd/system/ddclient.service
%dir /var/cache/ddclient

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.8.3-2
-	GA - Bump release of all rpms
* Tue Mar 22 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.8.3-1
- Initial packaging for Photon
