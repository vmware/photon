%global srcname requests-oauthlib
%global modname requests_oauthlib

Summary:    OAuthlib authentication support for Requests.
Name:       python3-requests-oauthlib
Version:    1.3.1
Release:    2%{?dist}
URL:        http://pypi.python.org/pypi/requests-oauthlib
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/requests/requests-oauthlib/archive/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.1-2
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.1-1
- Initial version, needed by syslog-ng.
