Summary:       Linux Containers File System
Name:          lxcfs
Version:       5.0.3
Release:       3%{?dist}
URL:           https://linuxcontainers.org/lxcfs/downloads/
Source0:       %{name}-%{version}.tar.gz
Group:         System Environment/Libraries
%define sha512 %{name}=967e60bd7ea545f1fcdd805adc0083e39684013c18f42a51753b5be8cdabfb86a652d02471a1f71c7b4fa756da09b72d324b724d68091d539edd10ea63add1fd
Vendor:        VMware, Inc.
Distribution:  Photon

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gcc meson python3-jinja2
BuildRequires: libtool
BuildRequires: fuse-devel
BuildRequires: systemd-devel
BuildRequires: help2man
Requires:      fuse
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Patch0: 0001-lxcfs-meson_build-Fix-service.patch

%description
LXCFS is a simple userspace filesystem designed to work around some current limitations of the Linux kernel.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
install -vdm755 %{buildroot}%{_sharedstatedir}/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_libdir}/%{name}/lib%{name}.so
%{_datadir}/%{name}/*.hook
%{_datadir}/lxc/config/common.conf.d/00-lxcfs.conf
%{_mandir}/man1/%{name}.1*
%dir %{_sharedstatedir}/%{name}

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 5.0.3-3
- Bump version as a part of meson upgrade
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 5.0.3-2
- Release bump for SRP compliance
* Tue Jan 24 2023 Ankit Jain <ankitja@vmware.com> 5.0.3-1
- Update to 5.0.3 and fixes services failure
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
