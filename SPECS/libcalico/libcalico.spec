%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library for interacting with Calico data model.
Name:           libcalico
Version:        0.19.0
Release:        1%{?dist}
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
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-backports.ssl_match_hostname
BuildRequires:  python-ConcurrentLogHandler
BuildRequires:  python-dnspython
BuildRequires:  python-docopt
BuildRequires:  python-etcd
BuildRequires:  python-netaddr
BuildRequires:  python-pip
BuildRequires:  python-prettytable
BuildRequires:  python-prometheus_client
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
BuildRequires:  python3
Requires:       python2
Requires:       python2-libs

%description
Library for interacting with Calico data model.

%prep
%setup

%build

%install
pip install --target=%{buildroot}%{python2_sitelib} .

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{python2_sitelib}/.libs_cffi_backend/libffi-72499c49.so.6.0.4

%changelog
*   Wed Aug 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19.0-1
-   libcalico for PhotonOS.
