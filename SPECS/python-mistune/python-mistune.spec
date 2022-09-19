Summary:        The fastest markdown parser in pure Python.
Name:           python3-mistune
Version:        2.0.4
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/mistune/
Source0:        https://files.pythonhosted.org/packages/source/m/mistune/mistune-%{version}.tar.gz
%define sha512  mistune=4d000c5791c29069b5f252f2aa5d361eb9cdf717d33f8d66dee8b4aa3bfe1242a572af63ca3dfd57324fac457fb9b5a9dff18e7da15f9036becd14cb27882dba

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
The fastest markdown parser in pure Python

The fastest markdown parser in pure Python with renderer features, inspired by marked.

%prep
%autosetup -n mistune-%{version}

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
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.4-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.8.3-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.8.3-1
- Update to version 0.8.3
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
- Initial packaging for Photon
