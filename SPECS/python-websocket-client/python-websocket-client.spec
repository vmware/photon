Name:           python3-websocket-client
Version:        1.4.1
Release:        2%{?dist}
Summary:        WebSocket client for python
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/websocket-client/websocket-client
Source0:        https://files.pythonhosted.org/packages/99/11/01fe7ebcb7545a1990c53c11f31230afe1388b0b34256e3fd20e49482245/websocket-client-%{version}.tar.gz
%define sha512  websocket-client=a2804421e97ccbfb61cb2e8a2be6ecd5d5d60210971e27ca4e00a4854fb49df2e3c87ec87c0ec11565d7ce03f419dc3cbd8c2402843a8fced49d75d65d07b502

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3

BuildArch:      noarch

%description
WebSocket client for python

%prep
%autosetup -n websocket-client-%{version}

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
%{_bindir}/wsdump

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.1-2
- Release bump for SRP compliance
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.1-1
- Update release to compile with python 3.11
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.57.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.57.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.53.0-3
- Mass removal python2.
* Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 0.53.0-2
- Add %check
* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.53.0-1
- Updated to release 0.53.0
* Thu Nov 30 2017 Xiaolin Li <xiaolinl@vmware.com> 0.44.0-1
- Update websocket_client to version 0.44.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
- Initial version of python WebSocket for PhotonOS.
