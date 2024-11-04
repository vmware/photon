Summary:        Utilities for loading kernel modules
Name:           kmod
Version:        30
Release:        5%{?dist}
URL:            http://www.kernel.org/pub/linux/utils/kernel/kmod
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
%define sha512 %{name}-%{version}=e2cd34e600a72e44710760dfda9364b790b8352a99eafbd43e683e4a06f37e6b5c0b5d14e7c28070e30fc5fc6ceddedf7b97f3b6c2c5c2d91204fefd630b9a3e

Source1: license.txt
%include %{SOURCE1}

Patch0: modinfo-show-signature-info-only-when-openssl.patch

BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

Requires: xz-libs
Requires: zlib

%description
The Kmod package contains libraries and utilities for loading kernel modules

%package        devel
Summary:        Header and development files for kmod
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
    --disable-manpages \
    --with-xz \
    --with-zlib \
    --disable-silent-rules

%make_build

%install
%make_install pkgconfigdir=%{_libdir}/pkgconfig %{?_smp_mflags}

install -vdm 755 %{buildroot}%{_sbindir}
for target in depmod insmod lsmod modinfo modprobe rmmod; do
  ln -srv %{buildroot}%{_bindir}/kmod %{buildroot}%{_sbindir}/$target
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_datadir}/bash-completion/completions/%{name}

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 30-5
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 30-4
- Bump version as a part of zlib upgrade
* Mon Mar 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 30-3
- Add support to print signature info when ssl libs are present
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 30-2
- bump version as part of xz upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 30-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 29-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 29-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 28-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 27-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 26-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 25-2
- Cross compilation support
* Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 25-1
- Updated to version 25
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 24-3
- Add devel package.
* Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 24-2
- Remove %check
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 24-1
- Updated to version 24
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21-4
- GA - Bump release of all rpms
* Thu Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 21-3
- Add patch for return code fix in error path
* Fri Mar 25 2016 Alexey Makhalov <amakhalov@vmware.com> 21-2
- /bin/lsmod -> /sbin/lsmod
* Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 21-1
- Updated to version 21
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 16-1
- Initial build. First version
