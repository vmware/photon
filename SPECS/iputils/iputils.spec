Summary:          Programs for basic networking
Name:             iputils
Version:          20221126
Release:          3%{?dist}
License:          BSD-3 and GPLv2+
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: %{name}-s%{version}.tar.gz
%define sha512 %{name}=7fdfd76e6f2977039bc0930a1a5451f17319bf17beefc429751d99ffe143a83344d5b4cdbf008627bd70caafeadaf906a8b7c00393fa819e50d6c02b512c367f

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

%prep
%autosetup -p1

%build
%{meson} \
  -DUSE_IDN=false \
  -DBUILD_MANS=false \
  -DBUILD_HTML_MANS=false

%{meson_build}

%install
%{meson_install}

%find_lang %{name}
ln -sf ping %{buildroot}%{_bindir}/ping6
ln -sf tracepath %{buildroot}%{_bindir}/tracepath6

%files
%defattr(-,root,root,-)
%{_datadir}/locale/*
%{_bindir}/ping6
%{_bindir}/tracepath6
%{_bindir}/tracepath
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/ping

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 20221126-3
- Bump version as a part of openssl upgrade
* Mon Oct 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 20221126-2
- Use relative path for ping6 symlink
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 20221126-1
- Automatic Version Bump
* Fri May 20 2022 Gerrit Photon <photon-checkins@vmware.com> 20211215-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 20200821-1
- Automatic Version Bump
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
