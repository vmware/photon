Summary: The Python Cryptography Toolkit.
Name:    pycrypto
Version: 2.7a1
Release: 3%{?dist}
License: UNKNOWN
URL: https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.7a1.tar.gz
Source: %{name}-%{version}.tar.gz
%define sha1 pycrypto=6326136d88e9a8f6dd8a41b91d56db8490ba2873
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
Requires:       python2
%description

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install -O1 --root=%{buildroot} --prefix=/usr

%check
python setup.py test

%files
%defattr(-,root,root)
%{_libdir}/python2.7/*

%changelog
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.7a1-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7a1-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7a1-1
-   Updated to version 2.7a1
*	Tue Dec 15 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial build.  First version
