%global build_if %{photon_subrelease} >= 92

Summary:       A Python module for decorators, wrappers and monkey patching
Name:          python3-wrapt
Version:       2.5.1
Release:       1%{?dist}
Group:         Development/Tools/Python
URL:           https://github.com/GrahamDumpleton/wrapt
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/GrahamDumpleton/wrapt/archive/refs/tags/%{version}.tar.gz#/wrapt-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gcc
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
Requires: python3

%description
The aim of the wrapt module is to provide a transparent object proxy for Python, which can be used as the basis for the construction
of function wrappers and decorator functions.

%prep
%autosetup -p1 -n wrapt-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{python3_sitearch}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.5.1-1
- Upgrade to 2.5.1
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.14.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.14.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.14.1-2
- Release bump for SRP compliance
* Mon Aug 29 2022 Srish Srinivasan <ssrish@vmware.com> 1.14.1-1
- Initial build. First version
