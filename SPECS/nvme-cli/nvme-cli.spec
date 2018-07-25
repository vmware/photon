Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       1.5
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       %{name}-%{version}.tar.gz
%define sha1   nvme-cli=16864b2df623e822ba2a69b0d5caa8b3f190acf0

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
*  Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
-  Resolved compilation error for aarch64
*  Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
-  Initial build
