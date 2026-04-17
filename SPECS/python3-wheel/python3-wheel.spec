%global build_if %{photon_subrelease} >= 92

%define srcname wheel

Name:           python3-wheel
Version:        0.46.3
Release:        1%{?dist}
Summary:        A built-package format for Python
URL:            https://pypi.org/project/wheel
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/pypa/wheel/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-setuptools

%define ExtraBuildRequires python3-pip

Requires:       python3
Provides:       python%{python3_version}dist(wheel) = %{version}-%{release}

%description
This library is the reference implementation of the Python wheel packaging standard, as defined in PEP 427.
It has two different roles. Firstly a setuptools extension for building wheels that provides the bdist_wheel setuptools command
Secondly, a command line tool for working with wheel files

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Fri Mar 27 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.46.3-1
- Upgrade to v0.46.3
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.37.1-5
- Bump version as a part of python3.14 upgrade
* Wed Feb 11 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.37.1-4
- Patch CVE-2022-40898
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.37.1-3
- Release bump for SRP compliance
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.37.1-2
- Spec fixes. Remove readme, license files.
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.37.1-1
- Initial Build
