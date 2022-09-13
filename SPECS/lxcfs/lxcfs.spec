Summary:       Linux Containers File System
Name:          lxcfs
Version:       5.0.0
Release:       1%{?dist}
URL:           https://linuxcontainers.org/lxcfs/downloads/
Source0:       %{name}-%{version}.tar.gz
License:       LGPL 2.1+
Group:         System Environment/Libraries
%define sha512 %{name}=f6ab0feea862812dde08dd828cb7843820a27f56ec88ef1bf264e3fe585037b9327849e4a31c629f2712c861cdc80d59ea15c190d875d48b2d446fe15d9e57b8
Vendor:        VMware, Inc.
Distribution:  Photon
BuildRequires: gcc meson python3-jinja2
BuildRequires: libtool
BuildRequires: fuse-devel
BuildRequires: systemd
Requires:      fuse

%description
LXCFS is a simple userspace filesystem designed to work around some current limitations of the Linux kernel.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%post
%systemd_post lxcfs.service

%preun
%systemd_preun lxcfs.service

%postun
%systemd_postun lxcfs.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/lib/systemd/system/%{name}.service
%{_bindir}/lxcfs
%{_libdir}/%{name}/liblxcfs.so
%{_datadir}/%{name}/*.hook
%{_datadir}/lxc/config/common.conf.d/00-lxcfs.conf

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 4.0.8-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 4.0.7-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.5-1
- Automatic Version Bump
* Wed Apr 22 2020 Anish Swaminathan <anishs@vmware.com>  4.0.3-1
- Initial release.
