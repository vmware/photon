%global build_if %{photon_subrelease} >= 91

%define srcname pyproject-hooks

Name:           python3-pyproject_hooks
Version:        1.2.0
Release:        2%{?dist}
Summary:        Wrappers to call pyproject.toml-based build backend hooks
URL:            https://pypi.org/project/pyproject_hooks
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/pypa/pyproject-hooks/archive/refs/tags/pyproject_hooks-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-Remove-flake8-from-dev-requires.patch

BuildRequires: python3-devel
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-flit-core

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

%description
This is a low-level library for calling build-backends in
pyproject.toml-based project. It provides the basic functionality
to help write tooling that generates distribution files from
Python projects.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
pip3 install testpath
%pytest
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.rst
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2.0-2
- Extended to build for subrelease 91 and above
* Fri Feb 13 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.0-1
- Initial build.
