Summary:        FSArchiver - Filesystem Archiver for Linux
Name:           fsarchiver
Version:        0.8.6
Release:        3%{?dist}
URL:            http://www.fsarchiver.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/fdupoux/fsarchiver/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=26a2d7a68d162aabb778b14f29c52cf8fbadb8147cf5eae592352a36fbf93cc45c08c241253bd8dfe8cd0b77d0f156afcc8d89e8d24a238fd4427cb479827f14

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  xz-devel
BuildRequires:  lzo-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  attr-devel

%description
FSArchiver is a system tool that allows you to save the contents of a file-system to a compressed archive file.
The file-system can be restored on a partition which has a different size and it can be restored on a different file-system.
Unlike tar/dar, FSArchiver also creates the file-system when it extracts the data to partitions.
Everything is checksummed in the archive in order to protect the data. If the archive is corrupt,
you just loose the current file, not the whole archive.
Fsarchiver is released under the GPL-v2 license.
You should read the Quick start guide if you are using FSArchiver for the first time.

%prep
%autosetup -p1

%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' src/filesys.c
sed -i '/unistd/a #include <sys/sysmacros.h>' src/devinfo.c
%configure \
    --bindir=/bin \
    --disable-silent-rules \
    --disable-lz4 \
    --disable-zstd

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make  %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_sbindir}/fsarchiver
%{_mandir}/man8/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.8.6-3
- Release bump for SRP compliance
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 0.8.6-2
- bump version as part of xz upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.8.6-1
- Automatic Version Bump
* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 0.8.5-2
- Fix compilation issue against glibc-2.28
* Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 0.8.5-1
- Bump to version 0.8.5
* Fri Apr 28 2017 Xiaolin Li <xiaolinl@vmware.com> 0.8.1-1
- Initial build.
