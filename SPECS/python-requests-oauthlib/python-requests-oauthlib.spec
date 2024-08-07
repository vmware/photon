%global srcname requests-oauthlib
%global modname requests_oauthlib

Summary:    OAuthlib authentication support for Requests.
Name:       python3-requests-oauthlib
Version:    1.3.1
Release:    1%{?dist}
License:    ISC
URL:        http://pypi.python.org/pypi/requests-oauthlib
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/requests/requests-oauthlib/archive/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=fb4b52edf5f3e4f82f9bedc13b4bc4032e629fd17fef62e72c9eeb734d1963c08c081c9a96db464539637c678e1f5b7f4bf9bb618a8bc1b6aa2024c7b5c620ea

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-oauthlib
BuildRequires: python3-requests
BuildRequires: python3-pip
BuildRequires: python3-wheel

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3-oauthlib
Requires: python3-requests
Requires: python3

%description
This project provides first-class OAuth library support for python-request.

%prep
%autosetup -n %{srcname}-%{version} -p1

# Remove bundled egg-info in case it exists
rm -rf %{srcname}.egg-info

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install requests-mock
%pytest -k "not testCanPostBinaryData and not test_content_type_override and not test_url_is_native_str"

%files
%defattr(-,root,root)
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.1-1
- Initial version, needed by syslog-ng.
