%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}

Name:           docker-py3
Version:        7.1.0
Release:        1%{?dist}
Summary:        Python API for docker
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/docker/docker-py

Source0: https://github.com/docker/docker-py/releases/download/%{version}/docker-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-hatchling
BuildRequires: python3-hatch-vcs
BuildRequires: python3-setuptools_scm
BuildRequires: python3-xml
BuildRequires: python3-macros

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-websocket-client
BuildRequires: python3-paramiko
%endif

Requires: python3
Requires: python3-requests >= 2.26.0
Requires: python3-urllib3 >= 1.26.0

BuildArch: noarch

%description
Python API for docker

%prep
%autosetup -n docker-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%{pytest} tests/unit
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Apr 09 2026 Mukul Sikka <mukul.sikka@broadcom.com> 7.1.0-1
- Update to 7.1.0
* Tue Mar 31 2026 Michelle Wang <michelle.wang@broadcom.com> 6.0.0-8
- Disable debuginfo package
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-7
- Bump version as a part of python3.14 upgrade
* Wed Jan 15 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-6
- Fix functionality break introduced by CVE-2024-35195 in python3-requests
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.0.0-5
- Release bump for SRP compliance
* Fri Nov 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-4
- Bump up as part of docker upgrade
* Tue Jun 04 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-3
- Add setuptools_scm and typing-extensions in BuildRequires
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 6.0.0-2
- Update release to compile with python 3.11
* Mon Oct 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.0.0-1
- Upgrade to v6.0.0
* Thu Oct 15 2020 Ashwin H <ashwinh@vmware.com> 4.3.1-1
- Upgrade to 4.3.1 release.
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0-2
- Mass removal python2
* Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 3.5.0-1
- Upgraded to 3.5.0 release.
* Fri Dec 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-3
- Added docker-pycreds3, python3-requests, python3-six,
- python3-websocket-client to requires of docker-py3
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.3.0-1
- Initial version of docker-py for PhotonOS.
