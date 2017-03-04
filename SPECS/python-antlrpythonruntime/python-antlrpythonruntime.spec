%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           python-antlrpythonruntime
Version:        3.1.2
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.antlr3.org/download/Python/antlr_python_runtime-%{version}.tar.gz
Source0:        antlr_python_runtime-%{version}.tar.gz
%define sha1    antlr_python_runtime=c57d4a03f80d157e9c0c1c8cd3038171900a364c

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  lapack-devel

Requires:       python2
Requires:       python2-libs

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%prep
%setup -q -n antlr_python_runtime-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
-   Initial packaging for Photon
