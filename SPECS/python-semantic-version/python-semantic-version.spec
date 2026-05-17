%global build_if %{photon_subrelease} >= 91

Name:           python3-semantic-version
Version:        2.10.0
Release:        4%{?dist}
Summary:        Library implementing the 'SemVer' scheme
Group:          Development/Languages/Python
Url:            https://github.com/rbarrois/python-semanticversion
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/7d/31/f2289ce78b9b473d582568c234e104d2a342fd658cc288a7553d83bb8595/semantic_version-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions
%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
This small python library provides a few tools to handle SemVer in Python.
It follows strictly the 2.0.0 version of the SemVer scheme.

%prep
%autosetup -n semantic_version-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pluggy atomicwrites more_itertools
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.10.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.10.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.10.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.10.0-1
- Initial Build
