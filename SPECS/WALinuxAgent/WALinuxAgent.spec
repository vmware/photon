Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.0.18
Release:        4%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            http://go.microsoft.com/fwlink/?LinkId=250998
Source0:        %{name}-%{version}.tar.gz
Patch0:         photondistroadd.patch
%define sha1 WALinuxAgent=76238745a0ec598920f37a6445e383dab23c9f1b
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  systemd
Requires:       python2
Requires:       python2-libs
Requires:       python-pyasn1
Requires:       openssh
Requires:       openssl
Requires:       util-linux
Requires:       sed
Requires:       grep
Requires:       sudo
Requires:       iptables
Requires:       systemd

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%setup -q
find . -type f -exec sed -i 's/\r//' {} +
find . -type f -exec chmod 0644 {} +
%patch -P 0 -p1

%pre -p /bin/sh

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --lnx-distro='photon' --init-system='systemd' --root=%{buildroot}
mkdir -p  %{buildroot}/%{_localstatedir}/log
mkdir -p -m 0700 %{buildroot}/%{_sharedstatedir}/waagent
touch %{buildroot}/%{_localstatedir}/log/waagent.log

%check
python2 setup.py check && python2 setup.py test

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service


%files
/usr/lib/systemd/system/*
%attr(0755,root,root) %{_sysconfdir}/udev/rules.d/99-azure-product-uuid.rules
%defattr(0644,root,root,0755)
%doc Changelog LICENSE-2.0.txt NOTICE README
%attr(0755,root,root) %{_sbindir}/waagent
%config(noreplace) %{_sysconfdir}/logrotate.d/waagent
%config %{_sysconfdir}/waagent.conf
%ghost %{_localstatedir}/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent


%changelog
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.18-4
- Use python2 explicitly to build
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.18-3
- GA - Bump release of all rpms
* Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-2
- Edit post scripts
* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-1
- Update to 2.0.18
* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.14-3
- Removed redundant requires 
* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum
* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial pacaking for Discus
