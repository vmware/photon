Summary:        Python package for providing Mozilla's CA Bundle
Name:           python3-certifi
Version:        2022.6.15
Release:        2%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/certifi/python-certifi/archive/certifi-%{version}.tar.gz
%define sha512  certifi=f2cf30dc0231a4ec9506746d7fdd96530efbe37f2f3beac7a897a428158175011dcabe8b97614c9cec811266057ac88c77d865b57b6644d7b03cd61ae3809308

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  ca-certificates
%if %{with_check}
BuildRequires:  python3-pytest
%endif

Requires:       ca-certificates

BuildArch:      noarch

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%prep
%autosetup -n certifi-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
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
