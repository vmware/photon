%global build_if %{photon_subrelease} >= 91

%global srcname tornado

Name:           python3-tornado
Version:        6.5.7
Release:        2%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Source0:        https://github.com/tornadoweb/tornado/archive/refs/tags/v6.5.7.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
Requires:       python3
Requires:       python3-libs

%description
Tornado is a Python web framework and asynchronous networking library

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
sh runtests.sh

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.5.7-2
- Extend to build for 91 and above
* Mon Aug 03 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.5.7-1
- Upgrade to version 6.5.7
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.2-9
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-8
- Bump version as a part of python3.14 upgrade
* Tue Jan 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-7
- Fix CVE-2025-67725 & CVE-2025-67726
* Thu Aug 14 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-6
- Fix CVE-2025-47287
* Tue May 06 2025 Tapas Kundu <tapas.kundu@broadcom.com> 6.2-5
- Release bump for SRP compliance
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-4
- Fix CVE-2024-52804
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 6.2-2
- Update release to compile with python 3.11
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 6.2-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 6.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.4-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 4.5.2-3
- Mass removal python2
* Tue Dec 17 2019 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-2
- To build python2 and python3 tornado packages
- To remove buildArch
* Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
- Initial version of python tornado for PhotonOS.
