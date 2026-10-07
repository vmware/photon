%global build_if %{photon_subrelease} >= 92

%define srcname geomet

Name:           python3-geomet
Version:        1.1.0
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://github.com/geomet/geomet

Source0: https://github.com/geomet/geomet/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires: python3
Requires: python3-click
Requires: python3-setuptools

BuildArch: noarch

%description
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
# this doesn't exist in current source archive
# will help in future
bash build-scripts/02-test.sh
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Wed Oct 07 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.0-1
- Upgrade to 1.1.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.3.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.3.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
- Initial packaging for Photon
