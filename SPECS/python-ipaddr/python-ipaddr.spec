%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-ipaddr
Version:        2.2.0
Release:        2%{?dist}
Url:            https://github.com/google/ipaddr-py
Summary:        Google's Python IP address manipulation library
License:        Apache2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
%define sha1    ipaddr=d2acca0d7eee9c21d103d11ddc1bd7a8cc9a5a27

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

Requires:       python3
Requires:	python3-libs

BuildArch:      noarch

%description
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.


%prep
%setup -q -n ipaddr-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 ipaddr_test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
-   Update to version 2.2.0
*   Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 2.1.11-4
-   Adding python 3 support.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.1.11-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.11-2
-   GA - Bump release of all rpms
*   Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
