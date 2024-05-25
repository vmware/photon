%define aufs_include_dir aufs-standalone-aufs%{version}/include

Summary:        Utilities for aufs
Name:           aufs-util
Version:        6.0
Release:        2%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/p/aufs/aufs-util/ref/master/branches/
Group:          System Environment
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=550f66d837fc840af1dfb3e518cbb6e6faff51ef46a1328719e6d04ac8aa8256c0fa75c878cb627d80ceb3caa2cc88198c09ed4bc0ea936824bfea87046467e6

Source1: aufs-standalone-aufs%{version}.tar.gz
%define sha512 aufs-standalone-aufs%{version}=7028ad5671a4d0b473e6c7613bad18a6fcf0b01d9e908b4d5851bba4f686c01da157ab55a9f15448ac9575e63fa5fe6d0ebee4a4f9d2f7a93d6902462d1b6612

Patch0: 0001-aufs_type.h-remove-__user.patch
Patch1: 0001-Makefile-remove-static-ldflag.patch
Patch2: 0002-Makefile-fix-sbin-dir-patch.patch

BuildArch:      x86_64

Requires:       linux

%description
These utilities are always necessary for aufs.

%prep
# Using autosetup is not feasible
%setup -q -a0 -a1
pushd aufs-standalone-aufs%{version}
%patch -P0 -p1
popd
%autopatch -p1 -m1 -M2

%build
export CPPFLAGS="-I ${PWD}/%{aufs_include_dir}/uapi"
%make_build

%install
export CPPFLAGS="-I ${PWD}/%{aufs_include_dir}/uapi"
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so*
%{_mandir}/*
%exclude %dir %{_libdir}/debug

%changelog
* Sat May 25 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.0-2
- Require linux
- Use patches instead of using sed commands to modify source at build time
* Tue Dec 13 2022 Ajay Kaher <akaher@vmware.com> 6.0-1
- Update to version 6.0
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
