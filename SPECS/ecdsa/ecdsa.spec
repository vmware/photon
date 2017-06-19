%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        ECDSA cryptographic signature library (pure python)
Name:           ecdsa
Version:        0.13
Release:        5%{?dist}
License:        MIT
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/ecdsa

Source0:        https://pypi.python.org/packages/source/e/ecdsa/%{name}-%{version}.tar.gz
%define         sha1 ecdsa=7bcf6d1773d08bcc4bdd28cd05c545969f5aa162

BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires:       python2

%description
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.

%package -n     python3-ecdsa
Summary:        python3-ecdsa
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%description -n python3-ecdsa

Python 3 version.

%prep
%setup -q

%build
python2 setup.py build
python3 setup.py build

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
python2 setup.py test
python3 setup.py test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{python2_sitelib}/*

%files -n python3-ecdsa
%defattr(-, root, root)
%{python3_sitelib}/*

%changelog
*   Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13-5
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13-4
-   Use python2 explicitly
*   Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13-3
-   Added python3 site-packages.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.13-2
-   GA - Bump release of all rpms
*   Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 0.13-1
-   Initial build.  First version
