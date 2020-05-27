%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-PyNaCl
Version:        1.3.0
Release:        1%{?dist}
Summary:        PyNaCl is a Python binding to libsodium
License:        Apache License, Version 2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/PyNaCl/PyNaCl-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        PyNaCl-%{version}.tar.gz
%define sha1    PyNaCl=c078953e5643ad4ff7881a4627f5147eb5c76cf4
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi
BuildRequires:  python-xml
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs


%description
Good password hashing for your software and your servers.

%package -n     python3-PyNaCl
Summary:        python-PyNaCl
Requires:       python3
Requires:       python3-libs

%description -n python3-PyNaCl
Python 3 version.

%prep
%setup -n PyNaCl-%{version}
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

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-PyNaCl
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
-   Initial packaging for Photon
