Name:           python3-click
Version:        8.0.1
Release:        1%{?dist}
Summary:        Composable command line interface toolkit
License:        BSD License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://palletsprojects.com/p/click

Source0: https://github.com/pallets/click/archive/refs/tags/click-%{version}.tar.gz
%define sha512 click=6a6d66c68dae4cfcfdab5d77dab4ab280b18f8e9ec326b4860012253d8f6b4fa57a5a3794ddebd228da85f893b0c6a737d8be3ad361d31098ef0a2ad684d6d0a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
It's the "Command Line Interface Creation Kit". It’s highly configurable but comes with sensible defaults out of the box.
It aims to make the process of writing command line tools quick and fun while also preventing any frustration caused by the inability to implement an intended CLI API.

%prep
%autosetup -p1 -n click-%{version}

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
%{python3_sitelib}/*

%changelog
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 8.0.1-1
- Initial packaging for Photon
