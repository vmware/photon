Name:           python-zope.interface
Version:        4.1.3
Release:        3%{?dist}
Url:            https://github.com/zopefoundation/zope.interface
Summary:        Interfaces for Python
License:        ZPL 2.1
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/z/zope.interface/zope.interface-%{version}.tar.gz
%define sha1 zope.interface=207161e27880d07679aff6d712ed12f55e3d91b6

BuildRequires: python2-devel
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires:       python2
Requires:		python2-libs

%description
This package is intended to be independently reusable in any Python project. It is maintained by the Zope Toolkit project.

This package provides an implementation of “object interfaces” for Python. Interfaces are a mechanism for labeling objects as conforming to a given API or contract. So, this package can be considered as implementation of the Design By Contract methodology support in Python.

For detailed documentation, please see http://docs.zope.org/zope.interface

%prep
%setup -q -n zope.interface-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
*       Mon Oct 04 2016 ChangLee <changlee@vmware.com> 4.1.3-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
-	GA - Bump release of all rpms
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
