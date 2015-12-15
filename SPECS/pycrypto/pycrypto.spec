Summary: The Python Cryptography Toolkit.
Name:    pycrypto
Version: 2.6.1
Release: 1%{?dist}
License: UNKNOWN
URL: https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz
Source: %{name}-%{version}.tar.gz
%define sha1 pycrypto=aeda3ed41caf1766409d4efc689b9ca30ad6aeb2
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

%files
%defattr(-,root,root)
%{_libdir}/python2.7/*

%changelog
*	Tue Dec 15 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial build.  First version
