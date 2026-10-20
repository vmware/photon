%global build_if %{photon_subrelease} >= 92

Name:           python3-hatch-vcs
Version:        0.5.0
Release:        1%{?dist}
Summary:        Hatch plugin for versioning with your preferred VCS
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/ofek/hatch-vcs
Source0: https://github.com/ofek/hatch-vcs/archive/refs/tags/v%{version}.tar.gz#/hatch_vcs-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3
Requires:       python3-hatchling
Requires:       python3-setuptools_scm

%description
This provides a plugin for Hatch that uses your preferred version control system (like Git) to determine project versions.

%prep
%autosetup -n hatch-vcs-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
python3 setup.py test

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.5.0-1
- Upgrade to 0.5.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.2.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.0-1
- Initial version
