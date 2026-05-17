%global build_if %{photon_subrelease} <= 90

Name:           python3-hatch-vcs
Version:        0.2.0
Release:        2.1.1%{?dist}
Summary:        Hatch plugin for versioning with your preferred VCS
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/ofek/hatch-vcs
Source0:        https://files.pythonhosted.org/packages/source/h/hatch_vcs/hatch_vcs-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-hatchling
BuildRequires:  python3-pluggy

Requires:       python3

%description
This provides a plugin for Hatch that uses your preferred version control system (like Git) to determine project versions.

%prep
%autosetup -n hatch_vcs-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.2.0-2.1.1
- Adjusted to build for subrelease 90
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.0-2.1
- Bump after moving to SPECS/91
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.2.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.0-1
- Initial version
