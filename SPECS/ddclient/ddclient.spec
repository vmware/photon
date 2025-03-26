Name:           ddclient
Version:        3.9.1
Release:        2%{?dist}
Url:            https://sourceforge.net/p/ddclient/wiki/Home/
Summary:        Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider
Group:          Applications
Source0:        http://downloads.sourceforge.net/project/ddclient/ddclient/ddclient-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Requires:       perl
Requires:       perl-IO-Socket-SSL
Requires:       perl-JSON-Any
Requires:       perl-Data-Validate-IP
Vendor:         VMware, Inc.
Distribution:   Photon

%description
DDclient is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider.
It was originally written by Paul Burry and is now mostly by wimpunk.
It has the capability to update more than just dyndns and it can fetch your WAN-ipaddress in a few different ways.

%prep
%autosetup -p1 -n %{name}-%{version}

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
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 3.9.1-2
- Release bump for SRP compliance
* Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 3.9.1-1
- Automatic Version Bump
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.9.0-2
- Add perl-Data-Validate-IP as a runtime dependency.
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 3.9.0-1
- Upgraded to version 3.9.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.8.3-3
- Remove BuildArch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.8.3-2
- GA - Bump release of all rpms
* Tue Mar 22 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.8.3-1
- Initial packaging for Photon
