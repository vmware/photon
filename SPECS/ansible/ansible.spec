Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.12.7
Release:        2%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ansible/ansible/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=8600fc96950ec1c0490bf3cbed88a1729bf4505b82879192ea9560ac6a90d27a382072e5d4aa92072f21e804867932c37ec7e5e75ffd08a383c4bf7d0e030607

Source1: macros.ansible
Source: tdnf.py

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-resolvelib

Requires: python3
Requires: python3-jinja2
Requires: python3-PyYAML
Requires: python3-xml
Requires: python3-paramiko
Requires: python3-resolvelib
Requires: python3-curses

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%package devel
Summary:        Development files for ansible packages
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for ansible packages

%prep
%autosetup -p1
cp -vp %{SOURCE2} lib/%{name}/modules/

%build
%{py3_build}

%install
%{py3_install}
install -Dpm0644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}
touch -r %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}

%files
%defattr(-, root, root)
%{_bindir}/*
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_rpmmacrodir}/macros.%{name}

%changelog
* Mon Nov 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.12.7-2
- Fix requires
- Fix an issue in upgrade using playbook.
* Thu Nov 24 2022 Nitesh Kumar <kunitesh@vmware.com> 2.12.7-1
- Version upgrade to v2.12.7
* Wed Sep 28 2022 Nitesh Kumar <kunitesh@vmware.com> 2.12.1-2
- Adding devel sub package
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.12.1-1
- Upgrade to v2.12.1 & fix tdnf module packaging
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.22-2
- Bump up to compile with python 3.10
* Wed Jun 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.9.22-1
- Bump version to 2.9.22 to fix CVE-2021-20178
* Fri Jul 03 2020 Shreendihi Shedi <sshedi@vmware.com> 2.9.10-1
- Upgrade to version 2.9.10
- Removed python2 dependancy
* Mon Apr 20 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-2
- Fix CVE-2020-1733, CVE-2020-1739
* Fri Apr 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-1
- Upgrade version to 2.8.10 & various CVEs fixed
* Sun Feb 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-3
- Fix 'make check'
* Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-2
- Fix for CVE-2019-14864
- Fix dependencies
- Patch to support tdnf operations
* Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-1
- Upgraded to version 2.8.3
* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.7.6-1
- Version update to 2.7.6, fix CVE-2018-16876
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.6.4-1
- Version update to 2.6.4
* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
- Version update to 2.4.0.0
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
- Use python2 explicitly
* Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
- Version update
* Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
- Initial build. First version
