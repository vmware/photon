Name:           python3-installer
Version:        0.7.0
Release:        1%{?dist}
Summary:        A library for installing Python wheels
License:        MIT
URL:            https://github.com/pypa/installer
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/installer/archive/refs/tags/installer-%{version}.tar.gz
%define sha512 installer=e89c2d28ca73d9c4291d645dda675fdcfcaba2e4f8765b9fa4a2f211e27711510f3d171b96a6b024c11808ba7f06b7b560a7cb31fafba815bd5c7396f26789f7

# Fix the build with Python 3.13 - merged upstream
# https://github.com/pypa/installer/commit/b23f89b10cf5
Patch0: Fix-removed-importlib.resources.read_binary-in-Pytho.patch

BuildArch:      noarch

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
%autosetup -p1 -n installer-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
%pytest

%files
%defattr(-,root,root)
%license LICENSE
%doc CONTRIBUTING.md README.md
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.0-1
- Initial version.
