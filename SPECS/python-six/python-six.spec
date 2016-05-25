Name:           python-six
Version:        1.10.0
Release:        2%{?dist}
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
Source0:        six-%{version}.tar.gz
%define sha1 six=30d480d2e352e8e4c2aae042cf1bf33368ff0920

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions. 

%prep
%setup -n six-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         1.10.0-2
-	GA - Bump release of all rpms
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.10.0-1
-	Upgrade version
* 	Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- 	Initial packaging for Photon
