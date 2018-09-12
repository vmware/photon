%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Show URLs for the python packages
Name:           python-pypi-show-urls
Version:        2.1.1
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/pypi-show-urls
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pypi-show-urls-%{version}.tar.gz
%define sha1    pypi-show-urls=0eed7aac7ddcd747f73b7806296f51360fbe37c9

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Shows information about where packages come from in Python.

%package -n     python3-pypi-show-urls
Summary:        python-pypi-show-urls
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-pypi-show-urls

Python 3 version.

%prep
%setup -q -n pypi-show-urls-%{version}
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

%check
python2 setup.py test
#python3 does not support zope module for tests

%files
%defattr(-,root,root)
%{python2_sitelib}/*
/usr/bin/pypi-show-urls

%files -n python3-pypi-show-urls
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> 2.1.1-1
-   Initial packaging for Photon.
