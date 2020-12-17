%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library for interacting with Calico data model.
Name:           libcalico
Version:        0.19.0
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/libcalico
Source0:        %{name}-%{version}.tar.gz
%define sha1 libcalico=c3d0f9f36930389fc3b6f1f2222ebc85440a50ee
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-backports.ssl_match_hostname
BuildRequires:  python3-ConcurrentLogHandler
BuildRequires:  python3-cffi
BuildRequires:  python3-pycrypto
BuildRequires:  python3-cryptography
BuildRequires:  python3-dnspython
BuildRequires:  python3-docopt
#BuildRequires:  python3-enum
BuildRequires:  python3-etcd
BuildRequires:  python3-idna
BuildRequires:  python3-ipaddress
BuildRequires:  python3-netaddr
BuildRequires:  python3-ndg-httpsclient
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pip
BuildRequires:  python3-prettytable
BuildRequires:  python3-prometheus_client
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyinstaller
BuildRequires:  python3-PyYAML
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-simplejson
BuildRequires:  python3-six
BuildRequires:  python3-subprocess32
BuildRequires:  python3-urllib3
BuildRequires:  python3-websocket-client
BuildRequires:  python3-appdirs
BuildRequires:  python3-virtualenv
BuildRequires:  python3
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
%define debug_package %{nil}

%description
Library for interacting with Calico data model.

%prep
%setup

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.19.0-4
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.19.0-3
-   openssl 1.1.1
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.19.0-2
-   Mass removal python2
*   Wed Aug 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19.0-1
-   libcalico for PhotonOS.
