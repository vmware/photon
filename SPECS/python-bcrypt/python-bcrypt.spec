Name:           python3-bcrypt
Version:        3.2.2
Release:        2%{?dist}
Summary:        Good password hashing for your software and your servers.
Group:          Development/Languages/Python
Url:            https://github.com/pyca/bcrypt
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://github.com/pyca/bcrypt/archive/refs/tags/bcrypt-%{version}.tar.gz
%define sha512  bcrypt=2f3b88bffaa9ff820aba6fb3143253b7936a1440ae93caff13cbdff58c1f8427f132cce60299cda523659b7026751a954b476857f2b9841cdd2a1a50c430a626

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
%endif

Requires:       python3

%description
Good password hashing for your software and your servers.

%prep
%autosetup -n bcrypt-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.2.2-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.2-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.7-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.1.6-3
- Mass removal python2
* Tue Sep 03 2019 Shreyas B. <shreyasb@vmware.com> 3.1.6-2
- Fix make check errors.
* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 3.1.6-1
- Initial packaging for Photon
