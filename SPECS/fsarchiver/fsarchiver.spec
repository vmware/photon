Summary:        FSArchiver - Filesystem Archiver for Linux
Name:           fsarchiver
Version:        0.8.5
Release:        2%{?dist}
License:        GPL-2.0
URL:            http://www.fsarchiver.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/fdupoux/fsarchiver/releases/download/%{version}/fsarchiver-%{version}.tar.gz
%define sha1    fsarchiver=1d4cd8064b49213bc825e9439d940d2041e975e0

BuildRequires:  xz-devel
BuildRequires:  lzo-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  attr-devel

%description
FSArchiver is a system tool that allows you to save the contents of a file-system to a compressed archive file. The file-system can be restored on a partition which has a different size and it can be restored on a different file-system. Unlike tar/dar, FSArchiver also creates the file-system when it extracts the data to partitions. Everything is checksummed in the archive in order to protect the data. If the archive is corrupt, you just loose the current file, not the whole archive. Fsarchiver is released under the GPL-v2 license. You should read the Quick start guide if you are using FSArchiver for the first time.

%prep
%setup -q
%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' src/filesys.c
sed -i '/unistd/a #include <sys/sysmacros.h>' src/devinfo.c
./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --disable-silent-rules \
    --disable-lz4 \
    --disable-zstd
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_sbindir}/fsarchiver
%{_mandir}/man8/*

%changelog
*   Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 0.8.5-2
-   Fix compilation issue against glibc-2.28
*   Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 0.8.5-1
-   Bump to version 0.8.5
*   Fri Apr 28 2017 Xiaolin Li <xiaolinl@vmware.com> 0.8.1-1
-   Initial build.
