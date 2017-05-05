%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           python-numpy
Version:        1.12.1
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/numpy
Source0:        https://pypi.python.org/packages/a5/16/8a678404411842fe02d780b5f0a676ff4d79cd58f0f22acddab1b392e230/numpy-%{version}.zip 
%define sha1    numpy=50d8a6dc5d95c914119d21b0c047b9761bbccd59 

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  lapack-devel
BuildRequires:  unzip

Requires:       python2
Requires:       python2-libs

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%package -n     python3-numpy
Summary:        python-numpy
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-numpy
Python 3 version.

%prep
%setup -q -n numpy-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/f2py2

%files -n python3-numpy
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/f2py3

%changelog
*   Thu May 04 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-2
-   Fix typo in Source0
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-1
-   Upgrade version to 1.12.1
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
-   Initial packaging for Photon
