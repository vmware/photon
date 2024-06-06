%global srcname build

Name:           python3-build
Version:        1.2.1
Release:        1%{?dist}
Summary:        A simple, correct PEP517 package builder
License:        MIT
URL:            https://github.com/pypa/build
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=77003e16d3776c3a4be920251bf14650eea112b92d94116cb1893195b8e16aae57321206ae63267119247f2794f220c891b7d913e07a8258b313d34c07d54fe9

%if 0%{?with_check}
Patch0: 0001-Remove-coverage-and-uv-from-tests.patch
%endif

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-flit-core

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-tomli
BuildRequires: python3-pyproject_hooks
BuildRequires: python3-filelock
%endif

Requires: python3
Requires: python3-flit-core
Requires: python3-pyproject_hooks

%description
A simple, correct PEP517 package builder.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install pytest_mock flaky
# The skipped tests require internet or uv
%pytest -k "not (test_build_package or \
                 test_build_package_via_sdist or \
                 test_output[via-sdist-isolation] or \
                 test_output[wheel-direct-isolation] or \
                 test_wheel_metadata[True] or \
                 test_wheel_metadata_isolation or \
                 test_with_get_requires or \
                 test_build_sdist or \
                 test_build_wheel[from_sdist] or \
                 test_build_wheel[direct] or \
                 test_uv_impl_install_cmd_well_formed or \
                 test_venv_creation[uv-venv+uv-None] or \
                 test_requirement_installation or \
                 test_requirement_installation or \
                 test_external_uv_detection_success or \
                 test_output[False-via-sdist-isolation] or \
                 test_output[False-wheel-direct-isolation] or \
                 test_verbose_output or \
                 test_build_wheel[False-from_sdist] or \
                 test_build_wheel[False-direct] or \
                 test_wheel_metadata[False-True] or \
                 test_venv_creation[pip-virtualenv+pip-True] or \
                 test_venv_creation[pip-virtualenv+pip-None] or \
                 test_init[False] or \
                 test_output[False-via-sdist-no-isolation] or \
                 test_output[False-wheel-direct-no-isolation] or \
                 test_output[False-sdist-direct-no-isolation] or \
                 test_output[False-sdist-and-wheel-direct-no-isolation])"

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/pyproject-build
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.1-1
- Initial version.
