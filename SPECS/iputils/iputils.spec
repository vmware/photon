Summary:          Programs for basic networking
Name:             iputils
Version:          20210722
Release:          1%{?dist}
License:          BSD-3 and GPLv2+
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-s%{version}.tar.gz
%define sha1      iputils=6e1fd3915d10bb5b3f0613e90ea156f3dd408623

BuildRequires:    libcap-devel
BuildRequires:    libgcrypt-devel
BuildRequires:    ninja-build
BuildRequires:    meson
BuildRequires:    openssl-devel
BuildRequires:    iproute2

Requires:         libcap
Requires:         libgcrypt
Requires:         systemd

%description
The Iputils package contains programs for basic networking.

%package ninfod
Summary: Node Information Query Daemon

Requires: %{name} = %{version}-%{release}
Provides: %{_sbindir}/ninfod

%description ninfod
Node Information Query (RFC4620) daemon. Responds to IPv6 Node Information
Queries

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson -DBUILD_TRACEROUTE6=true -DUSE_IDN=false -DBUILD_MANS=false -DBUILD_HTML_MANS=false
%meson_build

%install
%meson_install

%find_lang %{name}

ln -sf ../bin/ping %{buildroot}%{_sbindir}/ping
ln -sf ../bin/ping %{buildroot}%{_sbindir}/ping6
ln -sf ../bin/traceroute6 %{buildroot}%{_sbindir}/traceroute6
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}/tracepath
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}/tracepath6
ln -sf ../bin/arping %{buildroot}%{_sbindir}/arping

%files -f %{name}.lang
%{_sbindir}/rdisc
%{_sbindir}/ninfod
%{_sbindir}/tracepath
%{_sbindir}/traceroute6
%{_sbindir}/arping
%{_sbindir}/ping
%{_sbindir}/ping6
%{_sbindir}/tracepath6

%{_bindir}/tracepath
%{_bindir}/traceroute6

%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/ping

%files ninfod
%attr(0755,root,root) %caps(cap_net_raw=ep) %{_sbindir}/ninfod
%{_sysconfdir}/init.d/ninfod.sh

%changelog
* Wed Aug 04 2021 Susant Sahani <ssahani@vmware.com> 20210722-1
- Update version, modernize spec file. Use ldconfig scriptlets and autosetup
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20200821-1
- Automatic Version Bump
* Wed Aug 12 2020 Tapas Kundu <tkundu@vmware.com> 20190709-2
- Fix variable name collision with libcap update
* Mon Jul 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20190709-1
- Automatic Version Bump
* Thu Oct 10 2019 Tapas Kundu <tkundu@vmware.com> 20180629-2
- Provided ping6 as symlink of ping
* Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 20180629-1
- Updated to version 20180629
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 20151218-4
- Remove openssl and gnutls deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20151218-3
- GA - Bump release of all rpms
* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 20151218-2
- Fixing permissions for binaries
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 20151218-1
- Updated to version 2.4.18
* Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 20121221-1
- Initial build. First version
