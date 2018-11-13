%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-zope.interface
Version:        4.5.0
Release:        1%{?dist}
Url:            https://github.com/zopefoundation/zope.interface
Summary:        Interfaces for Python
License:        ZPL 2.1
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/z/zope.interface/zope.interface-%{version}.tar.gz
%define sha1    zope.interface=c580dead9e8afa8f602c1e1613bb22c2060cc700

BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
This package is intended to be independently reusable in any Python project. It is maintained by the Zope Toolkit project.

This package provides an implementation of “object interfaces” for Python. Interfaces are a mechanism for labeling objects as conforming to a given API or contract. So, this package can be considered as implementation of the Design By Contract methodology support in Python.

For detailed documentation, please see http://docs.zope.org/zope.interface

%package -n     python3-zope.interface
Summary:        python-zope.interface
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-zope.interface

Python 3 version.
%prep
%setup -q -n zope.interface-%{version}
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
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-zope.interface
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 4.5.0-1
-   Updated to release 4.5.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
-   Updated to version 4.3.3.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 4.1.3-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
-   GA - Bump release of all rpms
*   Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
