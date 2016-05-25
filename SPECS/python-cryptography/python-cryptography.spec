Summary:        Python cryptography library
Name:           python-cryptography
Version:        1.2.3
Release:        2%{?dist}
Url:            https://cryptography.io
License:        ASL 2.0
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha1 cryptography=a8a8083e70875423bd72899ca99890b788189205
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools
Requires:      python-cffi
BuildRequires: python-cffi
BuildRequires: openssl-devel
Requires:      openssl

Requires:       python2
Requires:       python2-libs

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.


%prep
%setup -q -n cryptography-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         1.2.3-2
-	GA - Bump release of all rpms
*	Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.2.3-1
-	Upgrade to 1.2.3
*	Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com> 1.2.2-1
-	Upgrade version to 1.2.2
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.2.1-1
-	Upgrade version
* 	Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.1-1
- 	Initial packaging for Photon
