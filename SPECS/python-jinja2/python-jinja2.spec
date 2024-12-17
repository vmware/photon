Summary:        A fast and easy to use template engine written in pure Python
Name:           python3-jinja2
Version:        3.1.2
Release:        5%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/pallets/jinja

Source0: https://github.com/pallets/jinja/archive/refs/tags/jinja-%{version}.tar.gz
%define sha512 jinja=50feebc7eed4c8b5bb0c2951784c1c115e3ee1c0e0c91bbf1884551b1312ef8fce24804a2ca1dfd8c543406529afe4817567c39e7cfd15028b54049853623144

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2024-22195.patch
Patch1: CVE-2024-34064.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-markupsafe >= 2.1.1

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3
Requires: python3-markupsafe >= 2.1.1

BuildArch: noarch

%description
Jinja2 is a template engine written in pure Python.
It provides a Django inspired non-XML syntax but supports inline
expressions and an optional sandboxed environment.

%prep
%autosetup -p1 -n jinja-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest tests
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/jinja2
%{python3_sitelib}/Jinja2-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.2-5
- Fix CVE-2024-22195.patch, CVE-2024-34064.patch
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.2-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.2-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.1.2-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.1.2-1
- Upgrade to v3.1.2, needed for ansible-2.13.3
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.11.2-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.10-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.10-1
- Update to version 2.10
* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.9.5-5
- Change python to python2
* Mon Jun 12 2017 Kumar Kaushik <kaushikk@vmware.com> 2.9.5-4
- Fixing import error in python3.
* Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.9.5-3
- BuildRequires python-markupsafe , creating subpackage python3-jinja2
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
- Fix arch
* Mon Mar 27 2017 Sarah Choi <sarahc@vmware.com> 2.9.5-1
- Upgrade version to 2.9.5
* Tue Dec 13 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.8-1
- Initial packaging for Photon
