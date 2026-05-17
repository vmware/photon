%global build_if %{photon_subrelease} >= 91

Name:           python3-backports_abc
Version:        0.5
Release:        4%{?dist}
Summary:        A backport of recent additions to the 'collections.abc' module.
Group:          Development/Languages/Python
Url:            https://github.com/cython/backports_abc
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pypi.python.org/packages/68/3c/1317a9113c377d1e33711ca8de1e80afbaf4a3c950dd0edfaf61f9bfe6d8/backports_abc-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description

%prep
%autosetup -n backports_abc-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
python3 tests.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.5-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.5-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.5-2
- Release bump for SRP compliance
* Wed Apr 17 2024 Prafful Mehrotra <prafful.mehrotra@broadcom.com> 0.5-1
- Bringing python-backports_abc to Ph5 for SALT 3006.7
