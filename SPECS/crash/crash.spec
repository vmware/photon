%define GDB_VERSION     10.2

Name:          crash
Version:       8.0.2
Release:       5%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://people.redhat.com/anderson
License:       GPL

Source0: http://people.redhat.com/anderson/%{name}-%{version}.tar.gz
%define sha512 %{name}=9ff24d1206e9376e83690f76c817a48a68ff6adce677fad70335a73550a59c9af6e4753c1199f22eafa60c137156313244bbf98ed01bc2b066f41d324738ef6b

Source2: https://ftp.gnu.org/gnu/gdb/gdb-%{GDB_VERSION}.tar.gz
%define sha512 gdb=aa89caf47c1c84366020377d47e7c51ddbc48e5b7686f244e38797c8eb88411cf57fcdc37eb669961efb41ceeac4181747f429625fd1acce7712cb9a1fea9c41

BuildRequires: binutils-devel
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: bison

Requires: binutils
Requires: ncurses-libs
Requires: zlib

%description
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      zlib-devel

%description devel
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

This package contains libraries and header files need for development.

%prep
%autosetup -p1
cp %{SOURCE2} .

%build
sed -i "s/tar --exclude-from/tar --no-same-owner --exclude-from/" Makefile

%make_build \
    GDB=gdb-%{GDB_VERSION} \
    RPMPKG=%{version}-%{release}

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man8 \
         %{buildroot}%{_includedir}/%{name} \
         %{buildroot}%{_libdir}/%{name}

%make_install %{?_smp_mflags}

install -pm 644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/%{name}

%clean
rm -rf "%{buildroot}"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

%changelog
* Mon Sep 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.2-5
- Fix devel package requires
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 8.0.2-4
- Bump version as a part of ncurses upgrade to v6.4
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.0.2-3
- Bump version as a part of zlib upgrade
* Mon Feb 20 2023 Tapas Kundu <tkundu@vmware.com> 8.0.2-2
- Add Bison in buildRequires.
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 8.0.2-1
- Automatic Version Bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 7.3.0-1
- Automatic Version Bump
* Mon Nov 30 2020 Alexey Makhalov <amakhalov@vmware.com> 7.2.9-1
- Version update
* Mon May 04 2020 Alexey Makhalov <amakhalov@vmware.com> 7.2.8-1
- Version update
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 7.2.3-1
- Upgrading to version 7.2.3
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-2
- Aarch64 support
* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-1
- Update version to 7.1.8 (it supports linux-4.9)
- Disable a patch - it requires a verification.
* Fri Oct 07 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-2
- gcore-support-linux-4.4.patch
* Fri Sep 30 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-1
- Update version to 7.1.5 (it supports linux-4.4)
- Added gcore plugin
- Remove zlib-devel requirement from -devel subpackage
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1.4-2
- GA - Bump release of all rpms
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1.4-1
- Updated to version 7.1.4
* Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 7.1.3-1
- Initial build. First version
