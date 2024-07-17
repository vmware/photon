%define GCORE_VERSION   1.6.3
%define GDB_VERSION     10.2

Name:          crash
Version:       8.0.2
Release:       2%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://people.redhat.com/anderson/
License:       GPL

Source0:       http://people.redhat.com/anderson/crash-%{version}.tar.gz
%define sha512 crash=9ff24d1206e9376e83690f76c817a48a68ff6adce677fad70335a73550a59c9af6e4753c1199f22eafa60c137156313244bbf98ed01bc2b066f41d324738ef6b

Source1:       http://people.redhat.com/anderson/extensions/crash-gcore-command-%{GCORE_VERSION}.tar.gz
%define sha512 crash-gcore=697952b7c55af5e4a7528cdd6fe616411d5147979fc90da55c0a3cee44510f39846e99bff3ac701c1ed98ee2c5d125e77c332b1f5b0be6e0ea1d98cf5d547a15

Source2:       https://ftp.gnu.org/gnu/gdb/gdb-%{GDB_VERSION}.tar.gz
%define sha512 gdb=aa89caf47c1c84366020377d47e7c51ddbc48e5b7686f244e38797c8eb88411cf57fcdc37eb669961efb41ceeac4181747f429625fd1acce7712cb9a1fea9c41

%ifarch aarch64
Patch0:       gcore_defs.patch
%endif

BuildRequires: binutils
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: bison

Requires:      binutils
Requires:      ncurses-libs

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
# Using autosetup is not feasible
%setup -q
# Using autosetup is not feasible
%setup -q -a 1
%ifarch aarch64
pushd crash-gcore-command-%{GCORE_VERSION}
%patch0 -p1
popd
%endif

%build
sed -i "s/tar --exclude-from/tar --no-same-owner --exclude-from/" Makefile
cp %{SOURCE2} .
%make_build GDB=gdb-%{GDB_VERSION} RPMPKG=%{version}-%{release}
cd crash-gcore-command-%{GCORE_VERSION}
%ifarch x86_64
%make_build -f gcore.mk ARCH=SUPPORTED TARGET=X86_64
%endif
%ifarch aarch64
%make_build -f gcore.mk ARCH=SUPPORTED TARGET=ARM64
%endif

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man8 \
         %{buildroot}%{_includedir}/crash \
         %{buildroot}%{_libdir}/crash

%make_install %{?_smp_mflags}

install -pm 644 crash.8 %{buildroot}%{_mandir}/man8/crash.8
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash
install -pm 755 crash-gcore-command-%{GCORE_VERSION}/gcore.so %{buildroot}%{_libdir}/crash/

%clean
rm -rf "%{buildroot}"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/crash
%{_libdir}/crash/gcore.so
%{_mandir}/man8/crash.8.gz

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%changelog
* Wed Jul 17 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.0.2-2
- Add zlib-devel to devl package requires
* Wed Jun 14 2023 Harinadh D <hdommaraju@vmware.com> 8.0.2-1
- Version upgrade to 8.0.2
* Wed Jul 13 2022 Ankit Jain <ankitja@vmware.com> 7.3.2-1
- Version update to 7.3.2
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
