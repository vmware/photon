Name:           python3-click
Version:        8.0.1
Release:        2%{?dist}
Summary:        Composable command line interface toolkit
License:        BSD License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/s/click/click-%{version}.tar.gz
Source0:        click-%{version}.tar.gz
%define sha1    click=0998d30c09384201260d92705ce0223e9b97e31a

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
It's the "Command Line Interface Creation Kit". It’s highly configurable but comes with sensible defaults out of the box.
It aims to make the process of writing command line tools quick and fun while also preventing any frustration caused by the inability to implement an intended CLI API.

%prep
%autosetup -n click-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 8.0.1-2
-   Bump up to compile with python 3.10
*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 8.0.1-1
-   Initial packaging for Photon
