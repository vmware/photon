%define debug_package %{nil}

Summary:        Library for interacting with Calico data model.
Name:           libcalico
Version:        0.19.0
Release:        3%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/libcalico
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=f38c850720b635c09fbc32f9be4830531f3cd47f77b1084f3150765d84f7e3ba5d135b7389fd4528c4f78593376907c1e5f7ac7eecfbea3d83bdf3c7d8134edf

BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  python2-devel
BuildRequires:  python-asn1crypto
BuildRequires:  python-backports.ssl_match_hostname
BuildRequires:  python-ConcurrentLogHandler
BuildRequires:  python-cffi
BuildRequires:  pycrypto
BuildRequires:  python-cryptography
BuildRequires:  python-dnspython
BuildRequires:  python-docopt
BuildRequires:  python-enum34
BuildRequires:  python-etcd
BuildRequires:  python-idna
BuildRequires:  python-ipaddress
BuildRequires:  python-netaddr
BuildRequires:  python-ndg-httpsclient
BuildRequires:  python-pyOpenSSL
BuildRequires:  python-pip
BuildRequires:  python-prettytable
BuildRequires:  python-prometheus_client
BuildRequires:  python-pyasn1
BuildRequires:  python-pycparser
BuildRequires:  python-pyinstaller
BuildRequires:  PyYAML
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-simplejson
BuildRequires:  python-six
BuildRequires:  python-subprocess32
BuildRequires:  python-urllib3
BuildRequires:  python-websocket-client
BuildRequires:  python-virtualenv
BuildRequires:  python3-devel

Requires:       python2
Requires:       python-setuptools

%description
Library for interacting with Calico data model.

%prep
%autosetup

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Tue Oct 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.19.0-3
- Bump version as a part of cryptography upgrade
* Sun Feb 12 2023 Prashant S Chauhan <psinghchuha@vmware.com> 0.19.0-2
- Bump up as part of python3-PyYAML update
* Wed Aug 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19.0-1
- libcalico for PhotonOS.
