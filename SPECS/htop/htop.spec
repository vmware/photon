Name:          htop
Version:       3.1.2
Release:       1%{?dist}
Summary:       Interactive process viewer
License:       GPLv2+
Group:i        Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://hisham.hm/htop/
Source0:       https://github.com/htop-dev/htop/archive/%{name}-%{version}.tar.gz
%define sha1   htop=b24053944897cd601532762de83f76df7b161833
BuildRequires: ncurses-devel
Requires:      ncurses-libs

%description
htop is an interactive text-mode process viewer for Linux, similar to
top.

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
* Mon Apr 11 2022 Shivani Agarwal <shivania2@vmware.com> 3.1.2-1
- htop initial build
