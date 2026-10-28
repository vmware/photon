%global build_if %{photon_subrelease} >= 92

Name:           python3-click
Version:        8.3.3
Release:        1%{?dist}
Summary:        Composable command line interface toolkit
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://palletsprojects.com/p/click

Source0: https://github.com/pallets/click/archive/refs/tags/%{version}.tar.gz#/click-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3

BuildArch:      noarch

%description
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
It's the "Command Line Interface Creation Kit". It’s highly configurable but comes with sensible defaults out of the box.
It aims to make the process of writing command line tools quick and fun while also preventing any frustration caused by the inability to implement an intended CLI API.

%prep
%autosetup -p1 -n click-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Oct 28 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.3.3-1
- Upgrade to v8.3.3
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 8.1.3-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.1.3-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.1.3-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 8.1.3-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 8.0.1-1
- Initial packaging for Photon
