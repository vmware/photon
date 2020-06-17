%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-PyNaCl
Version:        1.3.0
Release:        2%{?dist}
Summary:        PyNaCl is a Python binding to libsodium
License:        Apache License, Version 2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/PyNaCl/PyNaCl-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        PyNaCl-%{version}.tar.gz
%define sha1    PyNaCl=c078953e5643ad4ff7881a4627f5147eb5c76cf4
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs


%description
Good password hashing for your software and your servers.


%prep
%setup -n PyNaCl-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.3.0-2
-   Mass removal python2
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
-   Initial packaging for Photon
