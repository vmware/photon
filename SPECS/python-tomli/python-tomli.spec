%define srcname tomli

Name:       python3-tomli
Version:    2.0.1
Release:    1%{?dist}
Summary:    A little TOML parser for Python
License:    MIT
URL:        https://pypi.org/project/tomli
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/hukkin/tomli/archive/%{version}/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=a467f8d48cdbd7213bd9b6f85fd48ba142ab7c9656c40bb30785e1c4b37a9e29eaed420f183458ad20112baee8413ebbec87755332795c8f02235d1018c3aa5c

BuildArch: noarch

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
* Thu Jun 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.1-1
- Initial version. Needed by setuptools-rust.
