%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}



Name:           python-backports_abc
Version:        0.5
Release:        1%{?dist}
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


%package -n     python3-backports_abc
Summary:        python3 version A backport of recent additions to the 'collections.abc' module
BuildRequires:  python3-devel
Requires:       python3

%description -n python3-backports_abc
Python 3 version.

%prep
%setup -n backports_abc-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-backports_abc
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Dec 04 2018 Padmini Thirumalachar <pthirumalachar@vmware.com> 0.5-1
-   To build python2 and python3 backports_abc packages.
*   Wed Nov 29 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 0.5-1
-   Initial version of python backports_abc for PhotonOS.

