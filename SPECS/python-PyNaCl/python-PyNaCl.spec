%global build_if %{photon_subrelease} >= 92

Name:           python3-PyNaCl
Version:        1.6.2
Release:        1%{?dist}
Summary:        PyNaCl is a Python binding to libsodium
Group:          Development/Languages/Python
Url:            https://pypi.org/project/PyNaCl
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pyca/pynacl/archive/refs/tags/%{version}.tar.gz#/PyNaCl-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-Remove-undefined-__email__-from-nacl.__all__.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
BuildRequires:  curl-devel
Requires:       python3
Requires:       python3-libs

%description
Good password hashing for your software and your servers.

%prep
%autosetup -p1 -n pynacl-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
python3 setup.py test

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Oct 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.6.2-1
- Upgrade to 1.6.2
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.5.0-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.0-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.0-2
- Update release to compile with python 3.11
* Fri Oct 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.5.0-1
- Upgrade to latest version
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.3.0-2
- Mass removal python2
* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
- Initial packaging for Photon
