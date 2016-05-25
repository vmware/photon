Summary: ECDSA cryptographic signature library (pure python)
Name: ecdsa
Version: 0.13
Release: 2%{?dist}
License: MIT
Group: System Environment/Security
URL: https://pypi.python.org/pypi/ecdsa

Source0: https://pypi.python.org/packages/source/e/ecdsa/%{name}-%{version}.tar.gz
%define sha1 ecdsa=7bcf6d1773d08bcc4bdd28cd05c545969f5aa162

BuildArch: noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires: python2

%description
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.


%prep
%setup -q

%build
easy_install ./

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  0.13-2
-	GA - Bump release of all rpms
*	Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 0.13-1
-	Initial build.	First version