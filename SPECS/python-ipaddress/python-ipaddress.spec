Name:           python3-ipaddress
Version:        1.0.23
Release:        3%{?dist}
Summary:        Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ipaddress
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: ipaddress-%{version}.tar.gz
%define sha512 ipaddress=340e2a8698df1868038f55889671442eba17f06ec3f493759d8d0a9bf406eefbe1f67c14ca616f52e5bf2280942dcece7e89fb19de0923bee1ee20e60f48896e

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
IPv4/IPv6 manipulation library

%prep
%autosetup -p1 -n ipaddress-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.23-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.23-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.23-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.0.22-3
- Mass removal python2
* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-2
- Updated the license
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-1
- Update to version 1.0.22
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.18-2
- Change python to python2
* Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.18-1
- Initial packaging for Photon
