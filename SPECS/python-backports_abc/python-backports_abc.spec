Name:           python3-backports_abc
Version:        0.5
Release:        5%{?dist}
Summary:        A backport of recent additions to the 'collections.abc' module.
License:        PSFL
Group:          Development/Languages/Python
Url:            https://github.com/cython/backports_abc
Source0:        https://pypi.python.org/packages/68/3c/1317a9113c377d1e33711ca8de1e80afbaf4a3c950dd0edfaf61f9bfe6d8/backports_abc-0.5.tar.gz
%define sha1 backports_abc=91c000d7f18066f428b015caf5308ca34d492f77

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description

%prep
%autosetup -n backports_abc-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 tests.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.5-5
-   Bump up to compile with python 3.10
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.5-4
-   Mass removal python2
*   Tue Dec 17 2019 Vinothkumar D <vinothkumard@vmware.com> 0.5-3
-   To build python2 and python3 backports_abc packages.
*   Tue Dec 04 2018 Ashwin H <ashwinh@vmware.com> 0.5-2
-   Add %check
*   Wed Nov 29 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 0.5-1
-   Initial version of python backports_abc for PhotonOS.
