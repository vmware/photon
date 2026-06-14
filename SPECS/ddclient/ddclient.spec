%global debug_package %{nil}

Name:           ddclient
Version:        3.9.1
Release:        4%{?dist}
Url:            https://sourceforge.net/p/ddclient/wiki/Home/
Summary:        Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://downloads.sourceforge.net/project/ddclient/ddclient/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires:       perl
Requires:       perl-IO-Socket-SSL
Requires:       perl-Data-Validate-IP

%description
DDclient is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider.
It was originally written by Paul Burry and is now mostly by wimpunk.
It has the capability to update more than just dyndns and it can fetch your WAN-ipaddress in a few different ways.

%prep
%autosetup -p1

%install
install -vdm755 %{buildroot}%{_sbindir}
cp %{name} %{buildroot}%{_sbindir}/

install -vdm755 %{buildroot}%{_sysconfdir}/%{name}
install -vdm755 %{buildroot}%{_var}/cache/%{name}
install -vdm755 %{buildroot}%{_unitdir}

cp sample-etc_ddclient.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=Dynamic DNS Update Client
After=network.target
PartOf=network-online.target

[Service]
Type=forking
PIDFile=%{_rundir}/%{name}.pid
ExecStart=%{_sbindir}/%{name}

[Install]
WantedBy=network-online.target
EOF

%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}/%{name}.conf
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%dir %{_var}/cache/%{name}

%changelog
* Sun Jun 14 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.9.1-4
- Drop perl-JSON-Any dependency
* Tue Mar 31 2026 Michelle Wang <michelle.wang@broadcom.com> 3.9.1-3
- Disable debuginfo package
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
