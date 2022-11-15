Name:           python3-backports_abc
Version:        0.5
Release:        4%{?dist}
Summary:        A backport of recent additions to the 'collections.abc' module.
License:        PSFL
Group:          Development/Languages/Python
URL:            https://github.com/cython/backports_abc
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/cython/backports_abc/archive/refs/tags/backports_abc-%{version}.tar.gz
%define sha512 backports_abc=7c8a30857a1199e2539279d8fe82456db53fc2c8f0be2c696e029406756f6b7ad3628f4fc5203b58e6a89cb3a0bffdf85feb5af9e7d0bcd4ce0641ac469c9a1a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
Backport of recent additions to the "collections.abc" stdlib module (Py3.5)

%prep
%autosetup -p1 -n backports_abc-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 tests.py
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.5-4
- Mass removal python2
* Tue Dec 17 2019 Vinothkumar D <vinothkumard@vmware.com> 0.5-3
- To build python2 and python3 backports_abc packages.
* Tue Dec 04 2018 Ashwin H <ashwinh@vmware.com> 0.5-2
- Add %check
* Wed Nov 29 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 0.5-1
- Initial version of python backports_abc for PhotonOS.
