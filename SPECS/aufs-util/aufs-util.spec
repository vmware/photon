Summary:        Utilities for aufs
Name:           aufs-util
Version:        5.0
Release:        2%{?dist}
License:        GPLv2
URL:            http://aufs.sourceforge.net/
Group:          System Environment
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=89788181854a2d5ee9ce5883d3a40ad0ddceaf9898b94dbc714f88ef9b0be7975cf1f9a8a61bed5d127b120d61f2c728a181e42424b3655c3f92f2ad3966e0ff
Source1:        aufs5-standalone-5.7.tar.gz
%define sha512  aufs5-standalone-5.7=54bd4c85a92ae56bcf8f7b4de1989deee47c4248caf89548239c5598b016856c5c5285f1a4cccac40e4bcb4bf03d3dc461e0efbcd835ee8d86e55057d1841ec9

BuildArch:      x86_64

Requires:       linux-secure

%description
These utilities are always necessary for aufs.

%prep
# Using autosetup is not feasible
%setup -q
# Using autosetup is not feasible
%setup -q -T -D -b 1
sed -i 's/__user//' ../aufs5-standalone-aufs5.7/include/uapi/linux/aufs_type.h
sed -i '/override LDFLAGS += -static -s/d' Makefile

%build
make CPPFLAGS="-I ${PWD}/../aufs5-standalone-aufs5.7/include/uapi" DESTDIR=%{buildroot} %{?_smp_mflags}

%install
make CPPFLAGS="-I ${PWD}/../aufs5-standalone-aufs5.7/include/uapi" DESTDIR=%{buildroot} install %{?_smp_mflags}
mv %{buildroot}/sbin %{buildroot}%{_usr}

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*.so*
%{_mandir}/*
%exclude %dir %{_libdir}/debug

%changelog
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.0-2
- Fix binary path
* Fri Oct 09 2020 Ajay Kaher <akaher@vmware.com> 5.0-1
- Update to version 5.0
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 4.14-2
- Adding BuildArch
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 4.14-1
- Update to version 4.14
* Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-2
- Remove aufs source tarballs from git repo
* Fri Feb 10 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-1
- Initial build. First version
