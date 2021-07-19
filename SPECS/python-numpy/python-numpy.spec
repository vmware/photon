%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           python-numpy
Version:        1.8.2
Release:        3%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/numpy
Source0:        numpy-%{version}.tar.gz
%define sha1    numpy=9f7b889465263be527f615e4adae11446c2e7806
Patch0:         numpy-CVE-2017-12852.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python2
Requires:       python2-libs

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%package -n     python3-numpy
Summary:        python-numpy
Requires:       python3
Requires:       python3-libs

%description -n python3-numpy
Python 3 version.

%prep
%setup -q -n numpy-%{version}
%patch0 -p1

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
*   Mon Jul 19 2021 Nitesh Kumar <kunitesh@vmware.com> 1.8.2-3
-   Patched for CVE-2017-12852.
*   Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.2-2
-   Release bump to use python 3.5.4.
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
-   Initial packaging for Photon
