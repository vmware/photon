Summary:        FSArchiver - Filesystem Archiver for Linux
Name:           fsarchiver
Version:        0.8.0
Release:        1%{?dist}
License:        GPL-2.0
URL:            http://www.fsarchiver.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/fdupoux/fsarchiver/releases/download/%{version}/fsarchiver-%{version}.tar.gz
%define sha1    fsarchiver=57625b1c998d1812cd323ef1a65ba5700c18a807

BuildRequires:  xz-devel
BuildRequires:  lzo-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  attr

%description
FSArchiver is a system tool that allows you to save the contents of a file-system to a compressed archive file. The file-system can be restored on a partition which has a different size and it can be restored on a different file-system. Unlike tar/dar, FSArchiver also creates the file-system when it extracts the data to partitions. Everything is checksummed in the archive in order to protect the data. If the archive is corrupt, you just loose the current file, not the whole archive. Fsarchiver is released under the GPL-v2 license. You should read the Quick start guide if you are using FSArchiver for the first time.

%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix} \
    --bindir=/bin \
    --disable-silent-rules
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
*   Fri Apr 28 2017 Xiaolin Li <xiaolinl@vmware.com> 0.8.0-1
-   Initial build.
