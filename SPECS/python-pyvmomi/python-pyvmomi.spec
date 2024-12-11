Summary:        pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
Name:           python3-pyvmomi
Version:        8.0.2.0.1
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/pyvmomi
Source0:        pyvmomi-%{version}.tar.gz
%define sha512  pyvmomi=ed9a8115e70141805ef88d4b854d82f14b22c73bdcd701b9c2ad3e2da536505ecb3e20aff43cc8a9f3d4585daed27120e45636c0cd7af0afc70ae78c814aba64

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
%endif
Requires:       python3
BuildArch:      noarch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%prep
%autosetup -p1 -n pyvmomi-%{version}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.0.2.0.1-2
- Release bump for SRP compliance
* Sun May 26 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.0.2.0.1-1
- Update to 8.0.2.0.1
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.3-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 7.0.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 7.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-3
- Mass removal python2
* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-1
- Update to version 6.7.0.2018.9
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-1
- Initial packaging for Photon.
