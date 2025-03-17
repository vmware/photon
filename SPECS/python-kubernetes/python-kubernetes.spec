%global srcname kubernetes

Summary:    Python client for the kubernetes API.
Name:       python3-kubernetes
Version:    30.1.0
Release:    3%{?dist}
URL:        https://pypi.python.org/pypi/kubernetes
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/kubernetes-client/python/archive/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 30.1.0-3
- Release bump for SRP compliance
* Fri Aug 09 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 30.1.0-2
- Bump up as part of python3-urllib3 update
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 30.1.0-1
- Initial version. Needed by syslog-ng.
