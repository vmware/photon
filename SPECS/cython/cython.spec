%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        C extensions for Python
Name:           cython
Version:        0.28.5
Release:        1%{?dist}
Group:          Development/Libraries
License:        Apache License
URL:            http://cython.org/
Source0:         https://github.com/cython/cython/archive/Cython-%{version}.tar.gz
%define sha1 Cython=fc813f1cbc931ac230bbd6142b30f792af2db390
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:  python-xml
Requires:	python2

%description
Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

%prep
%setup -q -n cython-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python2_sitelib}/Cython-%{version}-*.egg-info
%{python2_sitelib}/Cython/*
%{python2_sitelib}/cython.py*
%{python2_sitelib}/pyximport/*


%changelog
*	Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 0.28.5-1
-	Upgraded to version 0.28.5
*       Thu Jul 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.25.2-2
-       Build using python2 explicity
*       Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 0.25.2-1
-       Update to 0.25.2
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.23.4-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.23.4-2
-	GA - Bump release of all rpms
* 	Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.23.4-1
- 	Initial build.
