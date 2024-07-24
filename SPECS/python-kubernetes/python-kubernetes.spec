%global srcname kubernetes

Summary:    Python client for the kubernetes API.
Name:       python3-kubernetes
Version:    30.1.0
Release:    1%{?dist}
License:    ASL 2.0
URL:        https://pypi.python.org/pypi/kubernetes
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/kubernetes-client/python/archive/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=26c07633529ebaf514900cca9e32b85cd87e59aa7eb458c75c281645a5564dca10baf5d84be3dd12192f119d37c6c72a2dd8563c497bc7ab549602c0cff08bda

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:  python3-certifi
Requires:  python3-six
Requires:  python3-dateutil
Requires:  python3-setuptools
Requires:  python3-PyYAML
Requires:  python3-google-auth
Requires:  python3-websocket-client
Requires:  python3-websocket-client
Requires:  python3-requests
Requires:  python3-requests-oauthlib
Requires:  python3-urllib3
Requires:  python3

%description
Python client for the kubernetes API.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
# no tests available in release tarball

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-*.egg-info

%changelog
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 30.1.0-1
- Initial version. Needed by syslog-ng.
