Name:           python3-backports_abc
Version:        0.5
Release:        1%{?dist}
Summary:        A backport of recent additions to the 'collections.abc' module.
License:        PSFL
Group:          Development/Languages/Python
Url:            https://github.com/cython/backports_abc
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pypi.python.org/packages/68/3c/1317a9113c377d1e33711ca8de1e80afbaf4a3c950dd0edfaf61f9bfe6d8/backports_abc-%{version}.tar.gz
%define sha512  backports_abc=7c8a30857a1199e2539279d8fe82456db53fc2c8f0be2c696e029406756f6b7ad3628f4fc5203b58e6a89cb3a0bffdf85feb5af9e7d0bcd4ce0641ac469c9a1a

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
* Wed Apr 17 2024 Prafful Mehrotra <prafful.mehrotra@broadcom.com> 0.5-1
- Bringing python-backports_abc to Ph5 for SALT 3006.7
