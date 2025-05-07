Name:           python3-M2Crypto
Version:        0.38.0
Release:        4%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/M2Crypto/0.26.0
Source0:        https://pypi.python.org/packages/11/29/0b075f51c38df4649a24ecff9ead1ffc57b164710821048e3d997f1363b9/M2Crypto-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:         0001-openssl-3.0.0-support.patch
%if 0%{?with_check}
Patch1:         makecheck.patch
%endif

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  swig
BuildRequires:  python3-xml
Requires:       python3
Requires:       openssl

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%prep
# Using autosetup is not feasible
%setup -q -n M2Crypto-%{version}
%patch -p1 0
%if 0%{?with_check}
%patch -p1 1
%endif

%build
CFLAGS="%{optflags}" python3 setup.py build --openssl=/usr/include --bundledlls

%install
rm -rf %{buildroot}
%py3_install

%check
python3 setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed May 07 2025 Tapas Kundu <tapas.kundu@broadcom.com> 0.38.0-4
- Remove python3-typing
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.38.0-3
- Release bump for SRP compliance
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.38.0-2
- Bump up version no. as part of swig upgrade
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.38.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.36.0-4
- Openssl 3.0.0 compatibility
* Tue Feb 16 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.36.0-3
- Fix make check
* Mon Jul 27 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.36.0-2
- Openssl 1.1.1 compatibility
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.36.0-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.30.1-4
- Mass removal python2
* Mon Oct 07 2019 Shreyas B. <shreyasb@vmware.com> 0.30.1-3
- Fixed makecheck errors.
* Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> 0.30.1-2
- Add %check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.30.1-1
- Update to version 0.30.1
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.26.0-2
- Remove BuildArch
* Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.26.0-1
- Initial packaging
