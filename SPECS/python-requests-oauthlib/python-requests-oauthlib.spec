%global build_if %{photon_subrelease} >= 92

%global srcname requests-oauthlib
%global modname requests_oauthlib

Summary:    OAuthlib authentication support for Requests.
Name:       python3-requests-oauthlib
Version:    2.0.0
Release:    1%{?dist}
URL:        http://pypi.python.org/pypi/requests-oauthlib
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/requests/requests-oauthlib/archive/refs/tags/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-oauthlib
BuildRequires: python3-requests
BuildRequires: python3-pip
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging

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
%{py3_build_wheel}

%install
%{py3_install_wheel}
%{py_byte_compile_and_ghost}

%check
pip3 install requests-mock
%pytest -k "not testCanPostBinaryData and not test_content_type_override and not test_url_is_native_str"

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 14 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-1
- Upgrade to 2.0.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.1-2
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.1-1
- Initial version, needed by syslog-ng.
