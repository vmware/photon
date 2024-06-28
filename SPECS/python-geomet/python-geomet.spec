%define srcname geomet

Name:           python3-geomet
Version:        0.3.0
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
License:        Apache Software License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://github.com/geomet/geomet

Source0: https://github.com/geomet/geomet/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=85380ed30adc027c6a97fa3b6e95034a9452617d26c6fb18d6700d5d4069acfde976a094a1a3f6e7240b9357e69f5dca85fa1c81d78102fa8a49b3186ccb82ac

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires: python3
Requires: python3-six
Requires: python3-click
Requires: python3-setuptools

BuildArch: noarch

%description
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
# this doesn't exist in current source archive
# will help in future
bash build-scripts/02-test.sh
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.3.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
- Initial packaging for Photon
