%global build_if %{photon_subrelease} >= 91

%define debug_package %{nil}

Summary:        PyInstaller hooks contrib is a required module during pyinstaller installation.
Name:           python3-pyinstaller-hooks-contrib
Version:        2025.8
Release:        3%{?dist}
Url:            https://pypi.org/project/pyinstaller-hooks-contrib
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/pyinstaller/pyinstaller-hooks-contrib/archive/refs/tags/pyinstaller-hooks-contrib-%{version}.tar.gz

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2025.8-3
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2025.8-2
- Bump version as a part of python3.14 upgrade
* Wed Sep 24 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2025.8-1
- Update to 2025.8
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2022.8-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2022.8-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2020.9-2
- Add Provides pyinstaller-hooks-contrib
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 2020.9-1
- Initial packaging for Photon.
