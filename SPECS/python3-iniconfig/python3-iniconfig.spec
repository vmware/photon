%global build_if %{photon_subrelease} >= 92

Summary:        iniconfig: brain-dead simple config-ini parsing
Name:           python3-iniconfig
Version:        2.3.0
Release:        1%{?dist}
URL:            http://github.com/RonnyPfannschmidt/iniconfig
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/RonnyPfannschmidt/iniconfig/archive/refs/tags/iniconfig-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-packaging
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools_scm

%if 0%{?with_check}
%define ExtraBuildRequires python3-pytest
%endif

Requires: python3

Provides: python%{python3_version}dist(iniconfig) = %{version}

%description
iniconfig is a small and simple INI-file parser module having a unique set of features:

1. tested against Python2.4 across to Python3.2, Jython, PyPy
2. maintains order of sections and entries
3. supports multi-line values with or without line-continuations
4. supports “#” comments everywhere
5. raises errors with proper line-numbers
6. no bells and whistles like automatic substitutions
7. iniconfig raises an Error if two sections have the same name.

%prep
%autosetup -p1 -n iniconfig-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%pytest
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/iniconfig*

%changelog
* Sat Mar 28 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.0-1
- Upgrade to v2.1.0
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.1-5
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.1-4
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.1-3
- Update release to compile with python 3.11
* Thu Aug 26 2021 Susant Sahani <ssahani@vmware.com> 1.1.1-2
- Use python macros
* Tue Nov 10 2020 Susant Sahani <ssahani@vmware.com> 1.1.1-1
- Initial rpm release.
