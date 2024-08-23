Summary:        Python package for providing Mozilla's CA Bundle
Name:           python3-certifi
Version:        2023.11.17
Release:        2%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/certifi/python-certifi/archive/certifi-%{version}.tar.gz
%define sha512  certifi=873eb3a34c5061f164484eec5bc659d4869882c96477395eec7d9d52242a033f9d82d293b07bcb094d04e62dc9af8a65caf2385a1a2a78c7058252af1b3d715b
Patch0:         CVE-2024-39689.patch

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
%py3_build

%install
%py3_install

%check
%py3_test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Aug 23 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2023.11.17-2
- Fix CVE-2024-39689
* Tue Dec 19 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2023.11.17-1
- Update to 2023.11.17
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2022.6.15-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2022.6.15-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2020.6.20-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 2018.08.24-2
- Mass removal python2
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2018.08.24-1
- Initial packaging
