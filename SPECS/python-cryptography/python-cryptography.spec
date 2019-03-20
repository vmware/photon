%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python cryptography library
Name:           python-cryptography
Version:        2.3.1
Release:        1%{?dist}
Url:            https://cryptography.io
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha1    cryptography=c550f9ba5a46ad33a0568edc2b9d0f4af3e4adab
#https://github.com/pyca/cryptography/pull/3278/commits/6779428e804d17cfb9f23a618b38e1089de93bdd
#Patch0:         clear_error_queue_at_startup.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi
BuildRequires:  openssl-devel
Requires:       openssl
Requires:       python-cffi
Requires:       python2
Requires:       python2-libs
Requires:       python-idna
Requires:       python-pyasn1
Requires:       python-ipaddress
Requires:       python-setuptools
Requires:       python-enum
Requires:       python-six

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-cryptography
Summary:        python-cryptography
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-cffi
Requires:       python3
Requires:       python3-libs
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-pyasn1
Requires:       python3-six

%description -n python3-cryptography

Python 3 version.

%prep
%setup -q -n cryptography-%{version}
#%patch0 -p1

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-cryptography
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
-   Updating to 2.3.1
*   Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-5
-   Release bump to use python 3.5.4.
*   Tue Jun 20 2017 Rongrong Qiu <rqiu@vmware.com> 1.7.2-4
-   Add python-six as requires.
*   Mon May 22 2017 Rongrong Qiu <rqiu@vmware.com> 1.7.2-3
-   Add python-enum as requires.
*   Mon Apr 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-2
-   Appy patch Refactor binding initialization to clear error queue at startup.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-1
-   Updated to version 1.7.2 and added python3 package.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.3-2
-   GA - Bump release of all rpms
*   Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.2.3-1
-   Upgrade to 1.2.3
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com> 1.2.2-1
-   Upgrade version to 1.2.2
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.2.1-1
-   Upgrade version
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.1-1
-   Initial packaging for Photon
