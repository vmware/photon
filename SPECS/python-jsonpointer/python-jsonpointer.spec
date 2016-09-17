Name:           python-jsonpointer
Version:        1.10
Release:        3%{?dist}
Summary:        Applying JSON Patches in Python
License:        Modified BSD License
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/j/jsonpointer/jsonpointer-%{version}.tar.gz
Source0:        jsonpointer-%{version}.tar.gz
%define sha1 jsonpointer=74db9372f71d8af9cd380e34fe1a0e274e6cd7cc

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902.

%prep
%setup -n jsonpointer-%{version}

%build
python setup.py build

%check
python tests.py

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/jsonpointer

%changelog
*       Mon Oct 04 2016 ChangLee <changlee@vmware.com> 1.10-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10-2
-	GA - Bump release of all rpms
*       Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10-1
-       Updated to version 1.10
*       Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-       Initial packaging for Photon
