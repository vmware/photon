%define srcname jinja2

Summary:        A fast and easy to use template engine written in pure Python
Name:           python3-jinja2
Version:        3.1.6
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/pallets/jinja

Source0: https://files.pythonhosted.org/packages/df/bf/f7da0350254c0ed7c72f3e33cef02e048281fec7ecec5f032d4aac52226b/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=bddd5e142f1462426c57b2efafdfafdfc6b66de257668707940896feae71eabdf19e0b6e34ef49b965153baf9b1eb59bb5a97349bb287ea0921dd2a751e967ab

BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-flit-core
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
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%if 0%{?with_check}
%check
%pytest tests
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}.dist-info

%changelog
* Mon Apr 07 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.6-1
- Update to 3.1.6. Fixes CVE-2024-56326, CVE-2024-56201 & CVE-2025-27516
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.1.2-2
- Fix CVE-2024-22195, CVE-2024-34064
* Thu Jan 04 2024 Nitesh Kumar <kunitesh@vmware.com> 3.1.2-1
- Version upgrade to v3.1.2 as required by ansible v2.14.12
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.11.2-2
- Update release to compile with python 3.10, use python3 macros file
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
