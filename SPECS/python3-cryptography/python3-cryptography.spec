Summary:        Python cryptography library
Name:           python3-cryptography
Version:        41.0.4
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/cryptography
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha512    cryptography=0c0a025ed5e39195561e5a6374463ee2261448657ebb89e39e761a5b02c701a8f804c1f84733cf8376e44a46784b2cc41134952c329987a96ee85cb4532c75cd
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  curl-devel

Requires:       python3
Requires:       python3-cffi
Requires:       python3-pycparser

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%prep
%autosetup -n cryptography-%{version}

%build
%py3_build

%install
%py3_install

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
pip3 install pretend pytest hypothesis iso8601 cryptography_vectors pytz
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Sep 25 2023 Felippe Burk <burkf@vmware.com> 41.0.4-1
-   update to version 41.0.4
*   Mon May 17 2021 Siju Maliakkal <smaliakkal@vmware.com> 2.8-2
-   Patch for CVE-2020-36242
*   Tue Mar 03 2020 Tapas Kundu <tkundu@vmware.com> 2.8-1
-   Update to version 2.8
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
-   Update to version 2.3.1
*   Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.3-1
-   Updated to version 2.0.3.
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
