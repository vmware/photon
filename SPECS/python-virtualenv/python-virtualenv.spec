%define srcname virtualenv

Name:           python3-virtualenv
Version:        20.16.3
Release:        4%{?dist}
Summary:        Virtual Python Environment builder
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=d3a90bab9862ea2a70e1dc429dff98a729425858a2153281cba4ecaf13107e6c3a43781e8c96b1f2a6c1ddd797de86bcfee8129a698e45d20eed76432efba5a6

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: python3-packaging
BuildRequires: python3-setuptools_scm
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires: python3-appdirs
BuildRequires: python3-pytest
BuildRequires: python3-platformdirs
BuildRequires: python3-filelock
BuildRequires: python3-distlib
%endif

Requires: python3
Requires: python3-appdirs
Requires: python3-distlib
Requires: python3-filelock
Requires: python3-platformdirs

BuildArch: noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install tomli flaky pytest-mock pytest-freezer
%pytest -k "not test_py_pyc_missing and not test_py_info_setuptools"

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
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
