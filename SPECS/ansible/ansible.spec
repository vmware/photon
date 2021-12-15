%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.10.16
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/ansible/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha1 %{name}=22eefc076bc1ebce0de86d32cacccea1b8330d22

Patch0:         Add-Photon-OS-tdnf-support.patch

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

Requires:       python3
Requires:       python3-libs
Requires:       python3-jinja2
Requires:       python3-PyYAML
Requires:       python3-xml
Requires:       python3-paramiko
%if %{with_check}
Requires:       python3-devel
%endif

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%autosetup -p1

%build
python3 setup.py build

%install
%{__rm} -rf %{buildroot}
python3 setup.py install -O1 --skip-build --root "%{buildroot}"

%check
python3 setup.py test

%files
%defattr(-, root, root)
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.10.16-1
- Upgrade to 2.10.16 & fix tdnf module packaging
* Mon Jun 14 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.10.10-1
- Bump version to fix CVE-2021-{20178, 20191}
* Thu Dec 17 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.18-1
- Automatic Version Bump
* Wed Oct 07 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-3
- Removed python2 dependency
* Mon Apr 20 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-2
- Fix CVE-2020-1733, CVE-2020-1739
* Fri Apr 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-1
- Upgrade version to 2.8.10 & various CVEs fixed
* Sun Feb 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-6
- Fix 'make check'
* Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-5
- Fix for CVE-2019-14864
* Mon Nov 18 2019 Tapas Kundu <tkundu@vmware.com> 2.8.3-4
- Added additional missing dependencies
* Fri Nov 08 2019 Tapas Kundu <tkundu@vmware.com> 2.8.3-3
- Fix dependencies
* Mon Sep 09 2019 Anish Swaminathan <anishs@vmware.com> 2.8.3-2
- Patch to support tdnf operations
* Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-1
- Upgraded to version 2.8.3
* Tue Apr 16 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.7.6-2
- Applied patch for CVE-2019-3828
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
