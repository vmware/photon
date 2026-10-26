Summary:        Python package for providing Mozilla's CA Bundle
Name:           python3-certifi
Version:        2026.10.23
Release:        1%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/certifi/python-certifi/archive/refs/tags/%{version}.tar.gz#/certifi-%{version}.tar.gz
%define sha512  certifi=f44a9f8b16ecd2b8abaa508bf6151574d62566ea782ede28a05caf8d974cc0d24d117384f32c7775784b41ba2efc9534d2a9d4f29fe7948b7727f2a7439175d6

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  ca-certificates
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       ca-certificates

BuildArch:      noarch

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%prep
%autosetup -p1 -n python-certifi-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
%{py3_test}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Oct 26 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2026.10.23-1
- Update to 2026.10.23, drops emSign Root CA - C1 and emSign ECC Root CA - C3
* Tue Oct 20 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 2026.10.19-1
- Update to 2026.10.19, drops eMudhra intermediate CA roots (Comodo AAA, emSign G3)
* Fri Aug 23 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2023.11.17-2
- Fix CVE-2024-39689
* Tue Dec 19 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2023.11.17-1
- Update to 2023.11.17
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2020.6.20-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2020.6.20-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 2018.08.24-2
- Mass removal python2
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2018.08.24-1
- Initial packaging
