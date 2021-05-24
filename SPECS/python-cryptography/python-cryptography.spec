%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python cryptography library
Name:           python-cryptography
Version:        1.9
Release:        1%{?dist}
Url:            https://cryptography.io
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha1    cryptography=a997853b98d454e4b9bc404390ce576fb5c2aeed
#https://github.com/pyca/cryptography/pull/3278/commits/6779428e804d17cfb9f23a618b38e1089de93bdd
Patch0:         cryptography-CVE-2020-36242.patch
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
Requires:       python-enum34
Requires:       python-six
Requires:       python-asn1crypto

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
Requires:       python3-asn1crypto

%description -n python3-cryptography

Python 3 version.

%prep
%setup -q -n cryptography-%{version}
%patch0 -p1

%build
python setup.py build

python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

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
pip install pretend pytest hypothesis iso8601 cryptography_vectors pytz
python setup.py test
pip3 install pretend pytest hypothesis iso8601 cryptography_vectors pytz
python3 setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-cryptography
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri May 21 2021 Siju Maliakkal <smaliakkal@vmware.com> 1.9-1
-   Upgraded to 1.9 for applying patch for CVE-2020-36242
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
