%define srcname M2Crypto

Name:           python3-M2Crypto
Version:        0.38.0
Release:        4%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
License:        MIT
URL:            https://gitlab.com/m2crypto/m2crypto
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://gitlab.com/m2crypto/m2crypto/-/archive/%{version}/M2Crypto-%{version}.tar.gz
%define sha512 %{srcname}=b1e24e3101ce0dd9f17be4cabeddc2ec0f1228b270d74ef2fb38bae8807c5025b031d0743185f06370786a3dd5c3f42129720534dcff07ea4de3c727613f8d20

BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-typing
BuildRequires: swig
BuildRequires: python3-xml

Requires: python3-typing
Requires: python3
Requires: openssl

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
CFLAGS="${CFLAGS} $(pkg-config --cflags openssl)"; export CFLAGS
LDFLAGS="${LDFLAGS} $(pkg-config --libs-only-L openssl)"; export LDFLAGS

%{py3_build}

%install
CFLAGS="${CFLAGS} $(pkg-config --cflags openssl)"; export CFLAGS
LDFLAGS="${LDFLAGS} $(pkg-config --libs-only-L openssl)"; export LDFLAGS

%{py3_install}

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
%python3 -munittest discover -v tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.38.0-4
- Bump version as a part of openssl upgrade
* Mon Aug 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.38.0-3
- Fix spec issues
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
