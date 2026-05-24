%global build_if %{photon_subrelease} >= 91

%global srcname hatch-fancy-pypi-readme

Name:           python3-hatch-fancy-pypi-readme
Version:        25.1.0
Release:        1%{?dist}
Summary:        Fancy PyPI READMEs with Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/hynek/hatch-fancy-pypi-readme
Source0:        https://github.com/hynek/hatch-fancy-pypi-readme/archive/25.1.0/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-installer

Requires:       python3

%description
hatch-fancy-pypi-readme is a Hatch metadata plugin for everyone who cares about
the first impression of their project’s PyPI landing page. It allows you to
define your PyPI project description in terms of concatenated fragments that
are based on static strings, files, and most importantly: parts of files
defined using cut-off points or regular expressions.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
python3 setup.py test

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Tue May 26 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 25.1.0-1
- Upgrade to latest 25.1.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 22.8.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 22.8.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 22.8.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.8.0-1
- Initial version
