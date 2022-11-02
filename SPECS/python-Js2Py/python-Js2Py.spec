Summary:        Pure Python JavaScript Translator/Interpreter.
Name:           python3-Js2Py
Version:        0.71
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Js2Py

Source0:        https://files.pythonhosted.org/packages/source/J/Js2Py/Js2Py-%{version}.tar.gz
%define sha512  Js2Py=32615af67d3ac237f55e2c98de399e153dbe36a30f9ca1f66a554ad8ff1016721d6121dd3123f969bc8df87f4b7585e8d6b9ca3159f82ec832a0822d44e6ae72

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-six
BuildRequires:  python3-py
BuildRequires:  python3-packaging
%if %{with_check}
BuildRequires:  python3-pyjsparser
%endif

Requires:       python3
Requires:       python3-six
Requires:       python3-tzlocal
Requires:       python3-pyjsparser

BuildArch:      noarch

%description
Pure Python JavaScript Translator/Interpreter.
Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3. Full support for ECMAScript 5.1, ECMA 6 support is still experimental.

%prep
%autosetup -p1 -n Js2Py-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%%check
#This package does not come with a test suite.

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
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
