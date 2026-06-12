%global build_if %{photon_subrelease} >= 91

Summary:        File System in Userspace (FUSE) utilities
Name:           fuse3
Version:        3.18.2
Release:        3%{?dist}
Url:            https://github.com/libfuse/libfuse
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libfuse/libfuse/archive/fuse-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# To break circualr dependency with e2fsprogs
%define ExtraBuildRequires meson, systemd-devel

Provides: fuse
Obsoletes: fuse

Requires: %{name}-libs = %{version}-%{release}

%description
With FUSE3 it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       systemd-devel
Requires:       pkg-config
Provides:       fuse-devel
Obsoletes:      fuse-devel

%description    devel
It contains the libraries and header files to create fuse applications.

%package        doc
Summary:        Documentation for %{name}
Conflicts:      %{name} < 3.18.2
Requires:       %{name} = %{version}-%{release}

%description    doc
%{summary}

%package        libs
Summary:        File System in Userspace (FUSE) v3 libraries
Conflicts:      %{name} < 3.18.2

%description    libs
%{summary}

%prep
%autosetup -n fuse-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

CONFIGURE_OPTS=(
  --prefix=%{_prefix}
  -D examples=false
)
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
%meson_install

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount3

rm -r %{buildroot}%{_sysconfdir}/init.d

%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/fuse.conf
%{_udevrulesdir}/99-%{name}.rules
%attr(4755,root,root) %{_bindir}/fusermount3
%{_sbindir}/mount.%{name}

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libfuse3.so

%files libs
%defattr(-, root, root)
%{_libdir}/libfuse3.so.*

%files doc
%defattr(-, root, root)
%{_datadir}/man/*

%changelog
* Fri Jun 12 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.18.2-3
- Add Obsoletes entries for fuse-devel
* Fri Jun 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.18.2-2
- Enable obsoletes
* Tue May 12 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.18.2-1
- Upgrade to v3.18.2
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.12.0-4
- Bump version as a part of meson upgrade
* Mon Dec 16 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 3.12.0-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.12.0-2
- Release bump for SRP compliance
* Wed Nov 30 2022 Piyush Gupta <gpiyush@vmware.com> 3.12.0-1
- Upgrade to 3.12.0.
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 3.11.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.9.4-3
- openssl 1.1.1
* Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com> 3.9.4-2
- Use meson and ninja build system
* Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9.4-1
- Automatic Version Bump
* Tue Apr 07 2020 Susant Sahani <ssahani@vmware.com> 3.9.1-1
- Update to 3.9.1
* Fri Nov 23 2018 Ashwin H <ashwinh@vmware.com> 3.2.6-2
- Fix %check
* Mon Sep 24 2018 Srinidhi Rao <srinidhir@vmware.com> 3.2.6-1
- Update to version 3.2.6.
* Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-2
- Move pkgconfig folder to devel package.
* Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
- Initial version.
