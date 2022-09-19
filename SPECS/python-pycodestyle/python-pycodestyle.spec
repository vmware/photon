Summary:        A tool to check your Python code
Name:           python3-pycodestyle
Version:        2.9.1
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pycodestyle-%{version}.tar.gz
%define sha512  pycodestyle=da1c67815b50d13c8eb70cebcc12c761a6407518a4ed4a8780ee7064089c9e89a5c3246d05f19916c0ec293fc1a372d3b2adb72e11f775b1cfbd1fbbe07a1a83

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%prep
%autosetup -n pycodestyle-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.9.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.6.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.5.0-2
- Mass removal python2
* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 2.5.0-1
- Initial packaging for Photon
