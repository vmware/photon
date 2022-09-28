Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.12.1
Release:        2%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha512  %{name}=6ffbb0106afff0e6cdb013d43e55d8e5d1857c64edd08efc9302d543891f1331cbbd95af3bc19f7058b831a2e6ce0d504e6116286c28a4c9dab9c08600469718

Source1:        macros.ansible

Patch0:         Add-Photon-OS-tdnf-support.patch

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros
BuildRequires:  python3-resolvelib

Requires:       python3
Requires:       python3-libs
Requires:       python3-jinja2
Requires:       python3-PyYAML
Requires:       python3-xml
Requires:       python3-paramiko
Requires:       python3-resolvelib

%if %{with_check}
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-cryptography
BuildRequires:  python3-PyYAML
BuildRequires:  python3-jinja2
%endif

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%package devel
Summary:        Development files for ansible packages
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for ansible packages

%prep
%autosetup -p1

%build
python3 setup.py build

%install
%{__rm} -rf %{buildroot}
python3 setup.py install -O1 --skip-build --root "%{buildroot}"
install -Dpm0644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}
touch -r %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}

%check
python3 setup.py test

%files
%defattr(-, root, root)
%{_bindir}/*
%{python3_sitelib}/*

%files devel
%defattr(-, root, root)
%{_rpmmacrodir}/macros.%{name}

%changelog
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
