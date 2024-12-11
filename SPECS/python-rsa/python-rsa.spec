%global srcname rsa

Summary:    Pure-Python RSA implementation
Name:       python3-rsa
Version:    4.9
Release:    2%{?dist}
URL:        http://stuvel.eu/rsa
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=85f359cc448a42f267f425fcf761597eeeab942523de49284b01d6ea2bcca8bddf0fac26926b487ae91c15889a7c4897a33ee00de859f28fe9cca19ef98c3f19

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pyasn1
BuildRequires: python3-pip
BuildRequires: python3-wheel

Requires: python3-pyasn1 >= 0.1.3
Requires: python3-setuptools
Requires: python3

%description
Python-RSA is a pure-Python RSA implementation. It supports encryption
and decryption, signing and verifying signatures, and key generation
according to PKCS#1 version 1.5. It can be used as a Python library as
well as on the command-line.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}
cp %{buildroot}%{_bindir}/pyrsa-priv2pub %{buildroot}%{_bindir}/pyrsa-priv2pub-3
cp %{buildroot}%{_bindir}/pyrsa-keygen %{buildroot}%{_bindir}/pyrsa-keygen-3
cp %{buildroot}%{_bindir}/pyrsa-encrypt %{buildroot}%{_bindir}/pyrsa-encrypt-3
cp %{buildroot}%{_bindir}/pyrsa-decrypt %{buildroot}%{_bindir}/pyrsa-decrypt-3
cp %{buildroot}%{_bindir}/pyrsa-sign %{buildroot}%{_bindir}/pyrsa-sign-3
cp %{buildroot}%{_bindir}/pyrsa-verify %{buildroot}%{_bindir}/pyrsa-verify-3

%check
# no test present in the release tarball

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_bindir}/pyrsa-priv2pub
%{_bindir}/pyrsa-keygen
%{_bindir}/pyrsa-encrypt
%{_bindir}/pyrsa-decrypt
%{_bindir}/pyrsa-sign
%{_bindir}/pyrsa-verify
%{_bindir}/pyrsa-priv2pub-3
%{_bindir}/pyrsa-keygen-3
%{_bindir}/pyrsa-encrypt-3
%{_bindir}/pyrsa-decrypt-3
%{_bindir}/pyrsa-sign-3
%{_bindir}/pyrsa-verify-3
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 4.9-2
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.9-1
- Initial version. Needed by syslog-ng.
