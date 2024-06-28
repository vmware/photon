Name:           python3-PyHamcrest
Version:        2.0.2
Release:        2%{?dist}
Summary:        Python Hamcrest framework for matcher objects
Group:          Development/Libraries
License:        BSD License (New BSD)
URL:            https://pypi.org/project/PyHamcrest
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/deepmerge/PyHamcrest-%{version}.tar.gz
%define sha512  PyHamcrest=f66d9119b93bdc29d2120cc58c1ba25f9777be7ec82fa888bfcbcc38f03bb0cbc59267d858f6a279bab5576061fe77618f5db320febf6f62d55b67b68be7c06a
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
PyHamcrest is a framework for writing matcher objects, allowing you to declaratively define “match” rules.

%prep
%autosetup -n PyHamcrest-%{version}

%build
%py3_build

%install
%py3_install

%check
#no test folder in source tar

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%doc README.rst
%doc LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.2-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.9.0-2
- Mass removal python2
* Fri Aug 30 2019 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
- Initial packaging for photon OS
