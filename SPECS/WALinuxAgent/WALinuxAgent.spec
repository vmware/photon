Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.4.0.2
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            https://github.com/Azure/WALinuxAgent
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=62b2819a63e615c8a9699685d6009820f025f212

Patch0:         Add-PhotonOS-support.patch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  systemd
BuildRequires:  python3-distro

Requires:       python3
Requires:       python3-libs
Requires:       python3-xml
Requires:       python3-pyasn1
Requires:       openssh
Requires:       openssl
Requires:       (util-linux or toybox)
Requires:       /bin/sed
Requires:       /bin/grep
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
%autosetup -p1 -n %{name}-%{version}

%pre -p /bin/sh

%build
python3 setup.py build -b py3

%install
python3 -tt setup.py build -b py3 install --prefix=%{_prefix} --lnx-distro='photonos' --root=%{buildroot} --force

mkdir -p %{buildroot}%{_localstatedir}/log \
         %{buildroot}%{_localstatedir}/opt/waagent/log \
         %{buildroot}%{_localstatedir}/log

mkdir -p -m 0700 %{buildroot}%{_sharedstatedir}/waagent
touch %{buildroot}%{_localstatedir}/opt/waagent/log/waagent.log
ln -sfv /opt/waagent/log/waagent.log %{buildroot}%{_localstatedir}/log/waagent.log

%check
python3 setup.py check && python3 setup.py test

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service

%files
/usr/%{_unitdir}/*
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/waagent
%attr(0755,root,root) %{_bindir}/waagent2.0
%config %{_sysconfdir}/waagent.conf
%dir %{_localstatedir}/opt/waagent/log
%{_localstatedir}/log/waagent.log
%ghost %{_localstatedir}/opt/waagent/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent
%{python3_sitelib}/*

%changelog
* Sat Nov 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0.2-1
- Upgrade to version 2.4.0.2
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.2.51-4
- Rectify previous fix
* Tue Nov 09 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.2.51-3
- Fix waagent.service to use python2
* Thu Mar 04 2021 Tapas Kundu <tkundu@vmware.com> 2.2.51-2
- Change all implementations of get_dhcp_pid to use run_command
* Wed Jan 06 2021 Tapas Kundu <tkundu@vmware.com> 2.2.51-1
- Version Bump
* Mon Aug 10 2020 Anisha Kumari <kanisha@vmware.com> 2.2.40-1
- updated to version 2.2.40 and removed patch for CVE-2019-0804
* Wed Apr 29 2020 Anisha Kumari <kanisha@vmware.com> 2.2.35-2
- Fix - added patch for CVE-2019-0804
* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 2.2.35-1
- Update to 2.2.35
* Tue Oct 23 2018 Anish Swaminathan <anishs@vmware.com> 2.2.22-1
- Update to 2.2.22
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.2.14-3
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.14-2
- Requires /bin/grep, /bin/sed and util-linux or toybox
* Thu Jul 13 2017 Anish Swaminathan <anishs@vmware.com> 2.2.14-1
- Update to 2.2.14
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
- Initial packaging
