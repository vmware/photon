%define debug_package %{nil}

Summary:        PyInstaller hooks contrib is a required module during pyinstaller installation.
Name:           python3-pyinstaller-hooks-contrib
Version:        2022.8
Release:        2%{?dist}
Url:            https://pypi.org/project/pyinstaller-hooks-contrib
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://files.pythonhosted.org/packages/ab/65/53a41d4788b8cbdd38c1f3404d07ca11c37e59a36170c10077e6ce001a3f/pyinstaller-hooks-contrib-%{version}.tar.gz
%define sha512  pyinstaller-hooks-contrib=ad918607cf551a5599d8ef71aa83a8b6d851e34912af0ce3fad1fc88e09e113fcbd7304c46173c3f130333ffe2fcd0bc7fd5745b17c3e18e82578a102157832c

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros

Requires:       python3

Provides:       python%{python3_version}dist(pyinstaller-hooks-contrib)

%description
Pyinstaller contrib hooks consist of  hooks for many packages, and allows PyInstaller to work with these packages seamlessly.

%prep
%autosetup -p1 -n pyinstaller-hooks-contrib-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2022.8-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2022.8-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2020.9-2
- Add Provides pyinstaller-hooks-contrib
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 2020.9-1
- Initial packaging for Photon.
