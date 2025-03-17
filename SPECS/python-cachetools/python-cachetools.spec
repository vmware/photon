%global srcname cachetools

Summary:    Extensible memoizing collections and decorators
Name:       python3-cachetools
Version:    5.4.0
Release:    2%{?dist}
URL:        https://pypi.python.org/pypi/%{srcname}
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/a7/3f/ea907ec6d15f68ea7f381546ba58adcb298417a59f01a2962cb5e486489f/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pip
BuildRequires: python3-wheel

Requires: python3

%description
This module provides various memoizing collections and decorators,
including a variant of the Python 3 Standard Library @lru_cache
function decorator.

This module provides multiple cache implementations based on different
cache algorithms, as well as decorators for easily memoizing function
and method calls.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
%{python3} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGELOG.rst PKG-INFO README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}.dist-info/

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.4.0-2
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.4.0-1
- Initial version. Needed by syslog-ng.
