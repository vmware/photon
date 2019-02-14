Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       1.6
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       %{name}-%{version}.tar.gz
%define sha1   nvme-cli=8e5928da01ad750c02a7c0f08d052bd9c12900b5

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
%{_sbindir}/nvme
%{_datadir}/*
%{_mandir}/man1/*

%changelog
*  Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
-  Upgrade to 1.6
*  Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
-  Resolved compilation error for aarch64
*  Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
-  Initial build
