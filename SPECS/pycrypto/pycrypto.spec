%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The Python Cryptography Toolkit.
Name:           python3-pycrypto
Version:        2.6.1
Release:        7%{?dist}
License:        Public Domain and Python
URL:            http://www.pycrypto.org/
Source0:        https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
%define         sha1 pycrypto=aeda3ed41caf1766409d4efc689b9ca30ad6aeb2
Patch0:         pycrypto-2.6.1-CVE-2013-7459.patch
Patch1:		pycrypto-2.6.1-CVE-2018-6594.patch
Patch2:         add_ccm_support_aes_only.patch
Patch3:         add_eax_authenticated_encryption.patch
Patch4:         add_support_for_siv.patch
Patch5:         add_gsm_support_aes.patch
Patch6:         fix_patch_errors.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-tools
Requires:       python3
%description
This is a collection of both secure hash functions (such as SHA256 and RIPEMD160), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).


%prep
%setup -q -n pycrypto-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1


%build
python3 setup.py build

%install
python3 setup.py install -O1 --root=%{buildroot} --prefix=/usr

%check
python3 setup.py test

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
*   Wed Aug 12 2020 Tapas Kundu <tkundu@vmware.com> 2.6.1-7
-   Require python3-tools for building.
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 2.6.1-6
-   Mass removal python2
*   Fri May 17 2019 Tapas Kundu <tkundu@vmware.com> 2.6.1-5
-   Add support for GCM mode (AES only).
*   Thu Nov 29 2018 Siju Maliakkal <smaliakkal@vmware.com> 2.6.1-4
-   Apply patch for CVE-2018-6594
*   Thu Jul 20 2017 Anish Swaminathan <anishs@vmware.com> 2.6.1-3
-   Apply patch for CVE-2013-7459
*   Thu Jul 13 2017 Divya Thaluru <dthaluru@vmware.com> 2.6.1-2
-   Downgraded to stable version 2.6.1
*   Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7a1-5
-   Using python2 explicitly while building
*   Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7a1-4
-   Added python3 site-packages.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.7a1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7a1-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7a1-1
-   Updated to version 2.7a1
*   Tue Dec 15 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial build.  First version
