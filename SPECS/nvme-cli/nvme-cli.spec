Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       1.12
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       %{name}-%{version}.tar.gz
%define sha1   nvme-cli=ec24fdc3944cff338170f8a98e95e9ebe90463f2

%description
NVM-Express user space tooling for Linux

%prep
%setup -q

%build
make

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%{_sbindir}/nvme
%{_mandir}/man1/nvme*.gz
%{_datadir}/bash-completion/completions/nvme
%{_datadir}/zsh/site-functions/_nvme
%dir %{_sysconfdir}/nvme
%{_sysconfdir}/nvme/*
%{_sysconfdir}/udev/*
%{_libdir}/dracut/dracut.conf.d/70-nvmf-autoconnect.conf
%{_libdir}/systemd/system/nvmefc-boot-connections.service
%{_libdir}/systemd/system/nvmf-autoconnect.service
%{_libdir}/systemd/system/nvmf-connect.target
%{_libdir}/systemd/system/nvmf-connect@.service

%changelog
*  Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.12-1
-  Automatic Version Bump
*  Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
-  Upgrade to 1.6
*  Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
-  Resolved compilation error for aarch64
*  Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
-  Initial build
