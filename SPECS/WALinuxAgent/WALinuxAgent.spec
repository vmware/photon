Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.9.1.1
Release:        3%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            https://github.com/Azure/WALinuxAgent
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/Azure/WALinuxAgent/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=3f44aecc16ac545db4b550586f168dbbdef34289aad6775973517bf645e5a1d486864c01e974f03a71b3e946c14e1ca140673a75c1cd602aac28725eaa68e83d

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: systemd-devel
BuildRequires: python3-distro
BuildRequires: python3-macros

Requires: python3
Requires: python3-xml
Requires: python3-pyasn1
Requires: openssh
Requires: openssl
Requires: util-linux
Requires: /bin/sed
Requires: /bin/grep
Requires: sudo
Requires: iptables
Requires: systemd
Requires: python3-distro

BuildArch: noarch

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%autosetup -p1

%build
%py3_build

%install
%{python3} setup.py install --skip-build install -O1 --lnx-distro='photonos' --root=%{buildroot}

mkdir -p %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/waagent/log \
         %{buildroot}%{_var}/log

mkdir -p -m 0700 %{buildroot}%{_sharedstatedir}/waagent
touch %{buildroot}%{_var}/opt/waagent/log/waagent.log
ln -sfv /opt/waagent/log/waagent.log %{buildroot}%{_var}/log/waagent.log

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_unitdir}/*
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/waagent
%attr(0755,root,root) %{_bindir}/waagent2.0
%config(noreplace) %{_sysconfdir}/waagent.conf
%dir %{_var}/opt/waagent/log
%{_var}/log/waagent.log
%ghost %{_var}/opt/waagent/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent
%{python3_sitelib}/*

%changelog
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.9.1.1-3
- Bump version as a part of util-linux upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.9.1.1-2
- Bump version as a part of openssl upgrade
* Thu Sep 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.9.1.1-1
- Upgrade to v2.9.1.1
* Tue Apr 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.3.0-4
- Add python3-distro to requires
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.3.0-3
- FIx requires
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.3.0-2
- Update release to compile with python 3.11
* Fri Aug 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7.3.0-1
- Upgrade to v2.7.3.0
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 2.7.1.0-1
- Automatic Version Bump
* Sat Nov 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0.2-1
- Upgrade to version 2.4.0.2
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.2.53.1-1
- Automatic Version Bump
* Mon Jan 11 2021 Tapas Kundu <tkundu@vmware.com> 2.2.51-1
- Version Bump
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.2.49.2-3
- Build with python 3.9
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.49.2-2
- openssl 1.1.1
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.49.2-1
- Automatic Version Bump
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 2.2.49-2
- Use python3.8
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.49-1
- Automatic Version Bump
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 2.2.35-3
- Use python3
* Wed Apr 29 2020 Anisha Kumari <kanisha@vmware.com> 2.2.35-2
- Added patch to fix CVE-2019-0804
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
- Added sha512sum
* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial packaging
