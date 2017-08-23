%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python cryptography library
Name:           python-cryptography
Version:        1.8.1
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/cryptography
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha1    cryptography=d15ffd42ca41260a61bc80cbeccf24e2dbf44253
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-cffi
BuildRequires:  openssl-devel

Requires:       python-cffi
Requires:       openssl
Requires:       python2
Requires:       python2-libs
Requires:       python-idna
Requires:       python-pyasn1
Requires:       python-ipaddress
Requires:       python-setuptools
Requires:       python-packaging
Requires:       python-enum34
Requires:       python-asn1crypto
Requires:       python-six

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-cryptography
Summary:        python-cryptography
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-pyasn1
Requires:       python3-six
Requires:       python3-packaging
Requires:       python3-asn1crypto

%description -n python3-cryptography

Python 3 version.

%prep
%setup -q -n cryptography-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=photon.com" \
    -keyout photon.key \
    -out photon.cert
openssl rsa -in photon.key -out photon.pem
mv photon.pem /etc/ssl/certs
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-cryptography
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.8.1-4
-   Added missing requires python-six and python-enum34
-   Removed python-enum from requires
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.1-2
-   Added missing requires python-enum
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
-   Updated to version 1.8.1.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-1
-   Updated to version 1.7.2 and added python3 package.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.2.3-3
-   Modified %check
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
