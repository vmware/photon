Name:           python3-websocket-client
Version:        0.57.0
Release:        2%{?dist}
Summary:        WebSocket client for python
License:        LGPL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/websocket-client/websocket-client

Source0: https://github.com/websocket-client/websocket-client/archive/refs/tags/websocket_client-%{version}.tar.gz
%define sha512 websocket_client=8677b00abbdd995ef1c2254f73a01713eb0707ee2549031f410205af7bbbf57b4730b38a78d683a90605c1412863f57a3829d8be1c058f3e9bfb177bd49c4525

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
%autosetup -n websocket_client-%{version}

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
%{_bindir}/wsdump.py

%changelog
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
