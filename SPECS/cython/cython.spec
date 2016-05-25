Summary:        C extensions for Python
Name:           cython
Version:        0.23.4
Release:        2%{?dist}
Group:          Development/Libraries
License:        Apache License
URL:            http://cython.org/
Source0:        http://cython.org/release/Cython-%{version}.tar.gz
%define sha1 Cython=fc574c5050cd5a8e34435432e2a4a693353ed807
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

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python_sitearch}/Cython-0.23.4-py2.7.egg-info
%{python_sitearch}/Cython/*
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport/*


%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.23.4-2
-	GA - Bump release of all rpms
* 	Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.23.4-1
- 	Initial build.
