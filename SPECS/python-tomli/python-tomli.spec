%global build_if %{photon_subrelease} >= 91

%define srcname tomli

Name:       python3-tomli
Version:    2.4.0
Release:    2%{?dist}
Summary:    A little TOML parser for Python
URL:        https://pypi.org/project/tomli
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

BuildArch: noarch

Source0: https://github.com/hukkin/tomli/archive/%{version}/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-flit-core
BuildRequires: python3-pip
BuildRequires: python3-wheel

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires: python3

%description
Tomli is a Python library for parsing TOML.
Tomli is fully compatible with TOML v1.0.0.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
%pytest

%clean
rm -rf %{buidlroot}

%files
%defattr(-,root,root)
%doc README.md
%doc CHANGELOG.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.4.0-2
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.4.0-1
- Initial version. Needed by setuptools-rust.
