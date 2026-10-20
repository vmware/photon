%global build_if %{photon_subrelease} >= 92

Name:           python3-discovery
Version:        1.6.4
Release:        1%{?dist}
Summary:        Python interpreter discovery
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/tox-dev/python-discovery
Source0: https://github.com/tox-dev/python-discovery/archive/refs/tags/%{version}.tar.gz#/python-discovery-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3
Requires:       python3-filelock >= 3.16.1

%description
Python interpreter discovery: find, query and select Python interpreters installed on a system, from the PATH, the Windows registry, the py launcher and other sources. It is the interpreter discovery logic used by virtualenv.

%prep
%autosetup -p1 -n python-discovery-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.6.4-1
- Initial build. First version
