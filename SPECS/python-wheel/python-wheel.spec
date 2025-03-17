%define srcname wheel

Name:           python3-wheel
Version:        0.37.1
Release:        3%{?dist}
Summary:        A built-package format for Python
URL:            https://pypi.org/project/wheel
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/wheel/archive/%{version}.tar.gz#/wheel-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Provides:       python%{python3_version}dist(wheel) = %{version}-%{release}
%description
This library is the reference implementation of the Python wheel packaging standard, as defined in PEP 427.
It has two different roles. Firstly a setuptools extension for building wheels that provides the bdist_wheel setuptools command
Secondly, a command line tool for working with wheel files

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.37.1-3
- Release bump for SRP compliance
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.37.1-2
- Spec fixes. Remove readme, license files.
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.37.1-1
- Initial Build
