%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-M2Crypto
Version:        0.32.0
Release:        1%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
License:        MIT
URL:            https://pypi.python.org/pypi/M2Crypto/0.26.0
Source0:        https://pypi.python.org/packages/11/29/0b075f51c38df4649a24ecff9ead1ffc57b164710821048e3d997f1363b9/M2Crypto-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
%define sha1 M2Crypto=b36c43373f952401b9cc190e4e5ddd09028e276b
BuildRequires:  python2-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python-setuptools
BuildRequires:  python-typing
BuildRequires:  swig
Requires:       python-typing
Requires:       python2

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%package -n     python3-M2Crypto
Summary:        python3 version of Crypto and SSL toolkit
BuildRequires:  python3-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python3-typing
Requires:       python3-typing
Requires:       python3

%description -n python3-M2Crypto
Python 3 version.

%prep
%setup -q -n M2Crypto-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="%{optflags}" python2 setup.py build --openssl=/usr/include --bundledlls
pushd ../p3dir
CFLAGS="%{optflags}" python3 setup.py build --openssl=/usr/include --bundledlls
popd

%install
rm -rf %{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-M2Crypto
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*    Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 0.32.0-1
-    Update to version 0.32.0
*    Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.26.0-1
-    Initial packaging
