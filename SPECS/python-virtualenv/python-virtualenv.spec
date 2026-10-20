%global build_if %{photon_subrelease} >= 92

%define srcname virtualenv

Name:           python3-virtualenv
Version:        21.14.5
Release:        1%{?dist}
Summary:        Virtual Python Environment builder
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/virtualenv/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-hatchling
BuildRequires: python3-hatch-vcs
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging

%if 0%{?with_check}
BuildRequires: python3-appdirs
BuildRequires: python3-pytest
BuildRequires: python3-platformdirs
BuildRequires: python3-filelock
BuildRequires: python3-distlib
BuildRequires: python3-discovery
%endif

Requires: python3
Requires: python3-distlib >= 0.3.7
Requires: python3-filelock >= 3.24.2
Requires: python3-packaging >= 23.1
Requires: python3-platformdirs >= 3.9.1
Requires: python3-discovery >= 1.6

BuildArch: noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
pip3 install tomli flaky pytest-mock pytest-freezer
%pytest -k "not test_py_pyc_missing and not test_py_info_setuptools"

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.14.5-1
- Upgrade to 21.14.5
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 20.16.3-8
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 20.16.3-7
- Bump version as a part of python3.14 upgrade
* Tue May 06 2025 Tapas Kundu <tapas.kundu@broadcom.com> 20.16.3-6
- Release bump for SRP compliance
* Mon Dec 16 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 20.16.3-5
- Fix CVE-2024-53899
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 20.16.3-4
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 20.16.3-3
- Use system provided packages to do offline build
* Tue Aug 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 20.16.3-2
- Add platformdirs to requires
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 20.16.3-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.1.0-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20.1.0-1
- Automatic Version Bump
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.32-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.31-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.30-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.28-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 16.0.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
- Update to version 16.0.0
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
- Initial version of python-virtualenv package for Photon.
