Name:           python3-pyproject_hooks
Version:        1.1.0
Release:        1%{?dist}
Summary:        Wrappers to call pyproject.toml-based build backend hooks
License:        MIT
URL:            https://pypi.org/project/pyproject_hooks
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/pyproject-hooks/archive/refs/tags/pyproject_hooks-%{version}.tar.gz
%define sha512 pyproject_hooks=256028d13adbe35126a63431a2a49e0c48adddce5ffc3ff2eebad368eee7ce52591ecfd8a8526876de20bc59dfc87156533d6a97b55538a739873e60f9509eff

Patch0: 0001-Remove-flake8-from-dev-requires.patch

BuildRequires: python3-devel
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-flit-core

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

BuildArch:      noarch

%description
This is a low-level library for calling build-backends in
pyproject.toml-based project. It provides the basic functionality
to help write tooling that generates distribution files from
Python projects.

%prep
%autosetup -p1 -n pyproject-hooks-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install testpath
%pytest

%files
%defattr(-,root,root)
%doc README.rst
%license LICENSE
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.0-1
- Initial build.
