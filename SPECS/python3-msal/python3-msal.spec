%global build_if %{photon_subrelease} >= 92

%global full_name microsoft-authentication-library-for-python

Name:           python3-msal
Version:        1.36.0
Release:        1%{?dist}
Summary:        Microsoft Authentication Library (MSAL) for Python
Group:          Development/Libraries/Python
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
URL:            https://github.com/AzureAD/microsoft-authentication-library-for-python
Source0:        https://github.com/AzureAD/%{full_name}/archive/%{version}/%{full_name}-%{version}.tar.gz

Source1:        license.txt
%include %{SOURCE1}

BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-PyJWT
BuildRequires:  python3-cryptography
Requires:       python3
Requires:       python3-cryptography
Requires:       python3-PyJWT
Requires:       python3-requests

%description
The Microsoft Authentication Library (MSAL) for Python enables applications to integrate
with the Microsoft identity platform by means of supporting signing in users or apps with
various Microsoft identities - Microsoft Entra ID, External identities, Microsoft Accounts
and Azure AD B2C - and obtain tokens to call various APIs such as Microsoft Graph or
custom APIs registered with the Microsoft identity platform. It is built using industry
standard OAuth2 and OpenID Connect protocols

%prep
%autosetup -p1 -n %{full_name}-%{version}
rm -rf .github .Pipelines docs/make.bat .readthedocs.yaml azure-pipelines.yml \
       sample spikes tests

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%clean
rm -rf %{buildroot}/*

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%doc README.md
%exclude %{python3_sitelib}/msal/__pycache__
%exclude %{python3_sitelib}/msal/oauth2cli/__pycache__
%{python3_sitelib}/msal
%{python3_sitelib}/msal-*.dist-info

%changelog
* Mon Apr 27 2026 Dweep Advani <dweep.advani@broadcom.com> 1.36.0-1
- Initial release
