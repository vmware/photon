%define python3_sitearch /usr/lib/python3.6/site-packages
Summary:        C extensions for Python
Name:           cython3
Version:        0.23.4
Release:        2%{?dist}
Group:          Development/Libraries
License:        Apache License
URL:            http://cython.org/
Source0:        http://cython.org/release/Cython-%{version}.tar.gz
%define sha1 Cython=fc574c5050cd5a8e34435432e2a4a693353ed807
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-libs
BuildRequires:  python-xml
Requires:	python3

%description
Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

%prep
%setup -q -n Cython-%{version}


%build
/usr/bin/python3 setup.py build

%install
/usr/bin/python3 setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/cython %{buildroot}%{_bindir}/cython3
mv %{buildroot}%{_bindir}/cythonize %{buildroot}%{_bindir}/cythonize3
mv %{buildroot}%{_bindir}/cygdb %{buildroot}%{_bindir}/cygdb3

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python3_sitearch}/*.egg-info
%{python3_sitearch}/Cython/*
%{python3_sitearch}/cython.py*
%{python3_sitearch}/pyximport/*
%{python3_sitearch}/__pycache__/*

%changelog
*       Tue Apr 25 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.23.4-2
-       Updated python3 site path
* 	Fri Jan 27 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.23.4-1
- 	Initial build.
