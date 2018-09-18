%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           python-numpy
Version:        1.15.1
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/numpy
Source0:        https://pypi.python.org/packages/a5/16/8a678404411842fe02d780b5f0a676ff4d79cd58f0f22acddab1b392e230/numpy-%{version}.zip 
%define sha1    numpy=2e7548d4972e5366dd8b30ca3639e243dae96af9

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
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-numpy
Python 3 version.

%prep
%setup -q -n numpy-%{version}

%build
# xlocale.h has been removed from glibc 2.26
# The above include of locale.h is sufficient
# Further details: https://sourceware.org/git/?p=glibc.git;a=commit;h=f0be25b6336db7492e47d2e8e72eb8af53b5506d */
sed -i "/xlocale.h/d" numpy/core/src/multiarray/numpyos.c
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose
mkdir test
pushd test
PYTHONPATH=%{buildroot}%{python2_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python2 -c "import numpy; numpy.test()"
popd

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
pushd test
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python3 -c "import numpy; numpy.test()"
popd

rm -rf test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/f2py2

%files -n python3-numpy
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/f2py3

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-1
-   Update to version 1.15.1
*   Fri Aug 25 2017 Alexey Makhalov <amakhalov@vmware.com> 1.12.1-5
-   Fix compilation issue for glibc-2.26
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.12.1-4
-   Fixed rpm check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.12.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu May 04 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-2
-   Fix typo in Source0
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-1
-   Upgrade version to 1.12.1
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
-   Initial packaging for Photon
