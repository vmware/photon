%global build_if %{photon_subrelease} >= 92

%define srcname installer

Name:           python3-installer
Version:        0.7.0
Release:        1%{?dist}
Summary:        A library for installing Python wheels
URL:            https://github.com/pypa/installer
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/pypa/installer/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Fix the build with Python 3.13 - merged upstream
# https://github.com/pypa/installer/commit/b23f89b10cf5
Patch0: Fix-removed-importlib.resources.read_binary-in-Pytho.patch

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-build

%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-tomli
%endif

%description
This is a low-level library for installing a Python package from
a wheel distribution. It provides basic functionality and abstractions
for handling wheels and installing packages from wheels.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
%pytest
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc CONTRIBUTING.md README.md
%{python3_sitelib}/*

%changelog
* Fri Feb 13 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.0-1
- Initial version.
