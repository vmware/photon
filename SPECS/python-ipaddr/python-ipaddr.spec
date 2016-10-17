Name:           python-ipaddr
Version:        2.1.11
Release:        3%{?dist}
Url:            https://github.com/google/ipaddr-py
Summary:        Google's Python IP address manipulation library
License:        Apache2
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
%define sha1 ipaddr=f9a16ddb3cf774b8dcf8894c2f4295c4e17d0ed3

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires:       python2
Requires:		python2-libs

BuildArch:      noarch

%description
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.

%prep
%setup -q -n ipaddr-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python ipaddr_test.py

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.1.11-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.11-2
-	GA - Bump release of all rpms
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
