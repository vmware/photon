Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.14.12
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ansible/ansible/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=4a44739bb10743b3bdf11de5d53ec5273f50f805a9f984ad5ddf330d1070205f03e8328d35bc66421b478ee55226e4e9b99b8ccd514c747e1cd688e620f4bd12

Source1: tdnf.py
Source2: macros.ansible
Source3: ansible_collection.py

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-resolvelib

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-jinja2 >= 3.1.2
BuildRequires: python3-PyYAML
BuildRequires: python3-pytest
BuildRequires: python3-cryptography
%endif

Requires: python3
Requires: python3-jinja2 >= 3.1.2
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
cp -vp %{SOURCE1} lib/%{name}/modules/

%build
%py3_build

%install
%py3_install
install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.%{name}
touch -r %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.%{name}
install -Dpm0744 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/%{name}_collection.py
touch -r %{SOURCE3} %{buildroot}%{_rpmconfigdir}/%{name}_collection.py

%files
%defattr(-, root, root)
%{_bindir}/*
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_rpmmacrodir}/macros.%{name}
%{_rpmconfigdir}/%{name}_collection.py

%changelog
* Thu Jan 04 2024 Nitesh Kumar <kunitesh@vmware.com> 2.14.12-1
- Version upgrade to v2.14.12 to fix CVE-2023-5764
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
