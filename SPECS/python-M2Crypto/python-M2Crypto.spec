%global build_if %{photon_subrelease} >= 92

Name:           python3-M2Crypto
Version:        0.47.0
Release:        2%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/M2Crypto/0.26.0
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: m2crypto-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -p1 -n m2crypto-%{version}

%build
CFLAGS="$CFLAGS `pkg-config --cflags openssl` -D__fds_bits=fds_bits" ; export CFLAGS
LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl` -D__fds_bits=fds_bits" ; export LDFLAGS
%py3_build

%install
CFLAGS="$CFLAGS `pkg-config --cflags openssl` -D__fds_bits=fds_bits" ; export CFLAGS
LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl` -D__fds_bits=fds_bits" ; export LDFLAGS
%py3_install

%check
python3 setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Mar 25 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 0.47.0-2
- Rename deprecated __fds_bits to fds_bits.
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.47.0-1
- Version upgrade
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
