%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           python3-numpy
Version:        1.19.2
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/numpy
Source0:        https://pypi.python.org/packages/a5/16/8a678404411842fe02d780b5f0a676ff4d79cd58f0f22acddab1b392e230/numpy-%{version}.zip
%define sha1    numpy=91073326e6241846ceabef8bc8ec1166336a10b0

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  lapack-devel
BuildRequires:  unzip
BuildRequires:  cython3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3
Requires:       python3-libs

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.


%prep
%setup -q -n numpy-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
mkdir test
pushd test
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose pytest
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python3 -c "import numpy; numpy.test()"
popd

rm -rf test

%files
%defattr(-,root,root,-)
%{_bindir}/f2py3
%{_bindir}/f2py
%{_bindir}/f2py3.8
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.19.2-2
-   openssl 1.1.1
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.2-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.1-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.15.1-3
-   Mass removal python2
*   Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-2
-   Fixed make check
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
