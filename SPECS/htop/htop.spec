Name:          htop
Version:       3.2.0
Release:       1%{?dist}
Summary:       Interactive process viewer
License:       GPLv2+
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://hisham.hm/htop/
Source0:       https://github.com/htop-dev/htop/archive/%{name}-%{version}.tar.gz
%define sha512 htop=174eaa7333fa60e40f67148560c53125e7aaf46a48e7f3ecfa2daa68553c94b3d076d03320afd479dcee07e739c0ff286a81b67cbc994782c33e798d3ed4605c
BuildRequires: ncurses-devel
Requires:      ncurses-libs

%description
htop is an interactive text-mode process viewer for Linux, similar to top.

%prep
%autosetup

%build
autoreconf -vfi

%configure \
        --enable-openvz \
        --enable-vserver \
        --enable-taskstats \
        --enable-unicode \
        --enable-native-affinity \
        --enable-oom \
        --with-sensors \
        --enable-cgroup

%make_build

%install
%make_install

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/htop
%{_datadir}/pixmaps/htop.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/htop.1*

%changelog
* Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Mon Apr 11 2022 Shivani Agarwal <shivania2@vmware.com> 3.1.2-1
- htop initial build
