Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       2.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       %{name}-%{version}.tar.gz
%define sha512 nvme-cli=24a00ee8e0fc963c1757797413ff5725cec18f821a714d6bbbf37906010d72934d6fdd7b466c085f13716a5279d1a7bd3254ee474e37a0ecd00a85ef23e12417
BuildRequires: meson
BuildRequires: cmake git
BuildRequires: pkg-config

%description
NVM-Express user space tooling for Linux

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot} %{?_smp_mflags}

%files
%defattr(-,root,root)
%doc README.md
%{_prefix}/etc/udev/rules.d/70-nvmf-autoconnect.rules
%{_prefix}/etc/udev/rules.d/71-nvmf-iopolicy-netapp.rules
%{_includedir}/json-c/arraylist.h
%{_includedir}/json-c/debug.h
%{_includedir}/json-c/json_c_version.h
%{_includedir}/json-c/json_config.h
%{_includedir}/json-c/json_inttypes.h
%{_includedir}/json-c/json_object.h
%{_includedir}/json-c/json_pointer.h
%{_includedir}/json-c/json_tokener.h
%{_includedir}/json-c/json_util.h
%{_includedir}/json-c/linkhash.h
%{_includedir}/json-c/printbuf.h
%{_includedir}/libnvme.h
%{_includedir}/nvme/fabrics.h
%{_includedir}/nvme/filters.h
%{_includedir}/nvme/ioctl.h
%{_includedir}/nvme/linux.h
%{_includedir}/nvme/log.h
%{_includedir}/nvme/tree.h
%{_includedir}/nvme/types.h
%{_includedir}/nvme/util.h
%{_libdir}/dracut/dracut.conf.d/70-nvmf-autoconnect.conf
%{_libdir}/libjson-c.so
%{_libdir}/libnvme.so
%{_libdir}/libnvme.so.1
%{_libdir}/libnvme.so.1.0.0
%{_libdir}/pkgconfig/json-c.pc
%{_libdir}/pkgconfig/libnvme.pc
%{_libdir}/systemd/nvmefc-boot-connections.service
%{_libdir}/systemd/nvmf-autoconnect.service
%{_libdir}/systemd/nvmf-connect.target
%{_libdir}/systemd/nvmf-connect@.service
%{_sbindir}/nvme
%{_datadir}/bash-completion/completions/nvme
%{_datadir}/zsh/site-functions/_nvme
%dir %{_sysconfdir}/nvme
%{_sysconfdir}/nvme/*

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0-1
-  Automatic Version Bump
*  Tue Apr 20 2021 Gerrit Photon <photon-checkins@vmware.com> 1.14-1
-  Automatic Version Bump
*  Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.13-1
-  Automatic Version Bump
*  Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.12-1
-  Automatic Version Bump
*  Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
-  Upgrade to 1.6
*  Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
-  Resolved compilation error for aarch64
*  Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
-  Initial build.
