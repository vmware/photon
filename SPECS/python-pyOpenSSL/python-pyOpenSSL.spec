%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python wrapper module around the OpenSSL library
Name:           python3-pyOpenSSL
Version:        18.0.0
Release:        4%{?dist}
Url:            https://github.com/pyca/pyopenssl
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/pyOpenSSL/pyOpenSSL-%{version}.tar.gz
%define sha1    pyOpenSSL=a41b82512585dd05a5370fb737f4eb4119030a38
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-six
BuildRequires:  python3-pycparser
BuildRequires:  python3-cffi
BuildRequires:  python3-idna
BuildRequires:  python3-pyasn1
BuildRequires:  python3-six
BuildRequires:  python3-packaging
BuildRequires:  python3-asn1crypto
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-cryptography
Requires:       python3-six

BuildArch:      noarch

%description
High-level wrapper around a subset of the OpenSSL library.


%prep
%setup -q -n pyOpenSSL-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pretend
$easy_install_3 flaky
$easy_install_3 pytest
PATH=%{buildroot}%{_bindir}:${PATH} \
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
    pytest
popd


%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 18.0.0-4
-   Mass removal python2
*   Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-3
-   Fix make check
*   Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
-   Update to version 18.0.0
*   Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 17.2.0-2
-   Added memory fix for X509StoreContext Class.
*   Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 17.2.0-1
-   Updated to version 17.2.0 and fixed make check.
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.2.0-5
-   Fixed runtime dependencies
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.2.0-3
-   Use python2 explicitly
*   Tue Feb 21 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-2
-   Add Requires for python-enum and python-ipaddress
*   Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-1
-   Initial packaging for Photon
