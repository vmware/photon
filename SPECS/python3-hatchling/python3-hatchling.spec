%global build_if %{photon_subrelease} >= 91

%define srcname hatchling

Name:           python3-hatchling
Version:        1.29.0
Release:        2%{?dist}
Summary:        The build backend used by Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/pypa/hatch

BuildArch:      noarch

Source0: https://github.com/pypa/hatch/releases/download/hatchling-v%{version}/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-pathspec
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy
BuildRequires:  python3-trove-classifiers

Requires:       python3
Requires:       python3-pluggy
Requires:       python3-pathspec
Requires:       python3-packaging
Requires:       python3-trove-classifiers

Provides:       python3dist(hatchling) = %{version}-%{release}

%description
This is the extensible, standards compliant build backend used by Hatch.

%prep
%autosetup -n %{srcname}-%{version}

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
%defattr(-,root,root)
%{_bindir}/hatchling
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.29.0-2
- Extended to build for subrelease 91 and above
* Fri Mar 27 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.29.0-1
- Upgrade to v1.29.0
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.11.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.11.1-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.11.1-1
- Initial version
