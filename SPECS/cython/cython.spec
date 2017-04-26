Summary:        C extensions for Python
Name:           cython
Version:        0.25.2
Release:        1%{?dist}
Group:          Development/Libraries
License:        Apache License
URL:            http://cython.org/
Source0:        http://cython.org/release/Cython-%{version}.tar.gz
%define sha1 Cython=e73f5afe89792df3467cc7bccd29fc01467fc28b
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:  python-xml
Requires:	python2

%description
Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

%prep
%setup -q -n Cython-%{version}


%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python_sitearch}/Cython-%{version}-*.egg-info
%{python_sitearch}/Cython/*
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport/*


%changelog
*       Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 0.25.2-1
-       Update to 0.25.2
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.23.4-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.23.4-2
-	GA - Bump release of all rpms
* 	Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.23.4-1
- 	Initial build.
