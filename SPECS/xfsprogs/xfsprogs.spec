Summary:        Utilities for managing the XFS filesystem
Name:           xfsprogs
Version:        6.0.0
Release:        2%{?dist}
License:        GPL+ and LGPLv2+
URL:            http://oss.sgi.com/projects/xfs
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.xz
%define sha512  %{name}=a3ddccdea1129038420d933f1e9ae8f9e75b3ad59fd0fe4c61b7a4dc6145f47b4262f68aefc3216d37cc33ee5643cd6f260ec83cd39d6b61a1cd046c03674ad8

BuildRequires: gettext
BuildRequires: inih-devel
BuildRequires: readline-devel
BuildRequires: userspace-rcu-devel
BuildRequires: util-linux-devel

Requires: inih
Requires: python3
Requires: util-linux-libs
Requires: userspace-rcu

%description
The xfsprogs package contains administration and debugging tools for the
XFS file system.

%package devel
Summary:    XFS filesystem-specific static libraries and headers
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Libraries and header files needed to develop XFS filesystem-specific programs.

%package lang
Summary:    Additional language files for xfsprogs
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of xfsprogs.

%prep
%autosetup -p1

%build
%configure \
    --enable-readline=yes \
    --enable-blkid=yes

make DEBUG=-DNDEBUG \
     INSTALL_USER=root \
     INSTALL_GROUP=root %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_docdir}/%{name}-%{version} \
             PKG_ROOT_LIB_DIR=%{_libdir} PKG_ROOT_SBIN_DIR=%{_sbindir} install %{?_smp_mflags}

make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_docdir}/%{name}-%{version} \
             PKG_ROOT_LIB_DIR=%{_libdir} PKG_ROOT_SBIN_DIR=%{_sbindir} install-dev %{?_smp_mflags}

find %{buildroot}%{_lib64dir} -name '*.la' -delete
find %{buildroot}%{_lib64dir} -name '*.a' -delete

%find_lang %{name}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/*
%{_sbindir}/*
%{_libdir}/*/*.cron
%{_mandir}/man2/*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_datadir}/%{name}/mkfs/*.conf
%exclude %{_docdir}/%{name}-%{version}/CHANGES.gz

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xfs
%{_libdir}/*.so*
%{_includedir}/xfs/*
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0.0-2
- Bump version as a part of gettext upgrade
* Fri Jan 06 2023 Oliver Kurth <okurth@vmware.com> 6.0.0-1
- update to 6.0.0
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 5.18.0-2
- Bump release as a part of readline upgrade
* Mon Jul 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.18.0-1
- Automatic version bump
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.8.0-2
- Fix binary path
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8.0-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 5.6.0-1
- Automatic Version Bump
* Tue Oct 22 2019 Prashant S Chauhan <psinghchauha@vmware.com> 4.18.0-2
- Removed %check since this package does not come with test suite
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.18.0-1
- Updated to latest version
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.10.0-3
- Use standard configure macros
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.10.0-2
- Ensure non empty debuginfo
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 4.10.0-1
- Updated to version 4.10.0.
* Fri Jan 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
- Initial build.  First version
