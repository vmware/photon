Summary:        Symbolic constants in Python.
Name:           python3-constantly
Version:        15.1.0
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/constantly
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        constantly-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.

%prep
%autosetup -n constantly-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 15.1.0-5
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 15.1.0-4
- Update release to compile with python 3.11
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 15.1.0-3
- Mass removal python2
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-1
- Initial packaging for Photon
