Name:           python3-click
Version:        8.1.3
Release:        2%{?dist}
Summary:        Composable command line interface toolkit
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://palletsprojects.com/p/click

Source0: https://github.com/pallets/click/archive/refs/tags/click-%{version}.tar.gz
%define sha512 click=be5b0c8b72ef7c10854f31406668ca4d6f826381deff10bb6a87a406166c09af97e2165f1327094d96abade15efb872892af37f20fdbc855b659cb2c7bd2f2c5

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.1.3-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 8.1.3-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 8.0.1-1
- Initial packaging for Photon
