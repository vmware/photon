%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-backports_abc
Version:        0.5
Release:        2%{?dist}
Summary:        A backport of recent additions to the 'collections.abc' module.
License:        PSFL
Group:          Development/Languages/Python
Url:            https://github.com/cython/backports_abc
Source0:        https://pypi.python.org/packages/68/3c/1317a9113c377d1e33711ca8de1e80afbaf4a3c950dd0edfaf61f9bfe6d8/backports_abc-0.5.tar.gz
%define sha1 backports_abc=91c000d7f18066f428b015caf5308ca34d492f77

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description


%prep
%setup -n backports_abc-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 tests.py

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Tue Dec 04 2018 Ashwin H <ashwinh@vmware.com> 0.5-2
-   Add %check
*   Wed Nov 29 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 0.5-1
-   Initial version of python backports_abc for PhotonOS.
