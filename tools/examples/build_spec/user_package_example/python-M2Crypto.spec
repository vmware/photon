Name:           python3-M2Crypto
Version:        0.36.0
Release:        1%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
License:        MIT
URL:            https://pypi.python.org/pypi/M2Crypto/0.26.0
Source0:        https://pypi.python.org/packages/11/29/0b075f51c38df4649a24ecff9ead1ffc57b164710821048e3d997f1363b9/M2Crypto-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing
BuildRequires:  swig
BuildRequires:  python3-xml
Requires:       python3-typing
Requires:       python3
Requires:       openssl
Patch0:         0001-openssl-3.0.0-support.patch

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
%patch0 -p1

%build
CFLAGS="%{optflags}" python3 setup.py build --openssl=/usr/include --bundledlls

%install
rm -rf %{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Oct 27 2022 User <user@example.org> 0.36.0-1
-   Initial build. First version
