%global build_if %{photon_subrelease} >= 92

Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.24.1
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pycryptodomex
Source0:        https://github.com/Legrandin/pycryptodome/archive/refs/tags/v%{version}x.tar.gz#/pycryptodomex-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-sphinx

Requires:  python3-sphinx
Requires:  python3-libs
Requires:  python3
Requires:  python3-setuptools

%description
Cryptographic library for Python

%prep
%autosetup -n pycryptodome-%{version}x

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
python3 setup.py test

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-%{version}.dist-info
%exclude %{python3_sitearch}/Cryptodome/SelfTest

%changelog
* Tue Oct 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.24.1-1
- Upgrade to 3.24.1
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.20.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-2
- Release bump for SRP compliance
* Mon Apr 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-1
- Update to 3.20.0, fixes CVE-2023-52323. Exclude SelfTest
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.0-1
- Update to 3.15.0
* Wed Feb 03 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
- Initial packaging for Photon
