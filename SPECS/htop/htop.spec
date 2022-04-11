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
%define sha512 htop=7e08b820042e480ca61137ff24b468804b49b95c1bbedaf82029dd79d29c2c541c5211284ec075692203788bbb868a9d4326ffd24c68419e22eec13ae5012700
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
