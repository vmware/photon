%global build_if %{photon_subrelease} >= 91

Name:           python3-hatch-fancy-pypi-readme
Version:        22.8.0
Release:        4%{?dist}
Summary:        Fancy PyPI READMEs with Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/hynek/hatch-fancy-pypi-readme
Source0:        https://files.pythonhosted.org/packages/source/h/hatch-fancy-pypi-readme/hatch_fancy_pypi_readme-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy

Requires:       python3

%description
hatch-fancy-pypi-readme is a Hatch metadata plugin for everyone who cares about
the first impression of their project’s PyPI landing page. It allows you to
define your PyPI project description in terms of concatenated fragments that
are based on static strings, files, and most importantly: parts of files
defined using cut-off points or regular expressions.

%prep
%autosetup -n hatch_fancy_pypi_readme-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{_bindir}/hatch-fancy-pypi-readme
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 22.8.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 22.8.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 22.8.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.8.0-1
- Initial version
