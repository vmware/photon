%global srcname google_auth

Summary:    Google Auth Python Library
Name:       python3-google-auth
Version:    2.32.0
Release:    2%{?dist}
URL:        https://github.com/googleapis/google-auth-library-python
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/googleapis/google-auth-library-python/archive/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:  noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pip
BuildRequires: python3-wheel

%if 0%{?with_check}
BuildRequires: python3-pyOpenSSL
BuildRequires: python3-pytest
BuildRequires: python3-cachetools
BuildRequires: python3-requests
BuildRequires: python3-pyasn1-modules
BuildRequires: python3-rsa
BuildRequires: python3-cryptography
%endif

Requires:  python3-pyasn1
Requires:  python3-pyasn1-modules
Requires:  python3-rsa
Requires:  python3-six
Requires:  python3-cachetools
Requires:  python3

%description
Google Auth Python Library

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
rm tests/transport/test__custom_tls_signer.py
pip3 install mock flask freezegun pyu2f pytest-localserver responses
%pytest

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%dir %{python3_sitelib}/google/
%{python3_sitelib}/google/auth
%{python3_sitelib}/google/oauth2
%{python3_sitelib}/google_auth-%{version}.dist-info/

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.32.0-2
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.32.0-1
- Initial version. Neede by syslog-ng.
