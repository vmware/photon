%define srcname Js2Py

Summary:        Pure Python JavaScript Translator/Interpreter.
Name:           python3-Js2Py
Version:        0.74
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Js2Py

Source0: https://files.pythonhosted.org/packages/source/J/Js2Py/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-Use-fips-compatible-algorithm.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-six
BuildRequires: python3-py
BuildRequires: python3-packaging

%if 0%{?with_check}
BuildRequires: python3-pyjsparser
BuildRequires: python3-numpy
%endif

Requires: python3
Requires: python3-numpy
Requires: python3-six
Requires: python3-tzlocal
Requires: python3-pyjsparser

BuildArch: noarch

%description
Pure Python JavaScript Translator/Interpreter.
Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3. Full support for ECMAScript 5.1, ECMA 6 support is still experimental.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
%{python3} simple_test.py

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.74-2
- Release bump for SRP compliance
* Sat Aug 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.74-1
- Upgrade to v0.74
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.71-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.71-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.70-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.66-2
- Mass removal python2
* Sun Nov 10 2019 Tapas Kundu <tkundu@vmware.com> 0.66-1
- Updated to version 0.66
* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 0.59-1
- Updated to version 0.59
* Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 0.50-1
- Initial packaging for Photon
