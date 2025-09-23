%define debug_package %{nil}

Summary:        PyInstaller hooks contrib is a required module during pyinstaller installation.
Name:           python3-pyinstaller-hooks-contrib
Version:        2024.8
Release:        1%{?dist}
Url:            https://pypi.org/project/pyinstaller-hooks-contrib
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/pyinstaller-hooks-contrib/pyinstaller_hooks_contrib-%{version}.tar.gz
%define sha512  pyinstaller_hooks_contrib=1998e0a39ee47ce9db977b3bff748838e342aea88386b85258353b8e31a93f8f0008defc14871d4991bbe01b3dc1533c072cd0b1cac2e3cce37d701369ef10e1
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros
Requires:       python3

%description
Pyinstaller contrib hooks consist of  hooks for many packages, and allows PyInstaller to work with these packages seamlessly.

%prep
%autosetup -n pyinstaller_hooks_contrib-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Sep 23 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2024.8-1
-   Upgrade to v2024.8 to fix compatibility with pyinstaller 6.10.0
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2020.9-2
-   Bump up to compile with python 3.10
*   Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 2020.9-1
-   Initial packaging for Photon.
