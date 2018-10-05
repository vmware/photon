Name:       btrfs-progs
Version:    4.10.2
Release:    2%{?dist}
Summary:    Userspace programs for btrfs
Group:      System Environment/Base
License:    GPLv2+
URL:        http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:    https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version}.tar.xz
%define sha1 btrfs-progs=c75d4ca843232a0da44e9a05aa073435ad9e4fdd
# e2fsprogs-1.44 compatibility
Patch0:     3a07b07b1a56f7d97390f66c01a5829abb2c5b70.patch
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  lzo-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libacl-devel
Requires:   e2fsprogs, lzo

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package devel
Summary:    btrfs filesystem-specific libraries and headers
Group:      Development/Libraries
Requires:   btrfs-progs = %{version}-%{release}

%description devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install btrfs-progs-devel if you want to develop
btrfs filesystem-specific programs.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
./autogen.sh
%configure
make DISABLE_DOCUMENTATION=1 %{?_smp_mflags}

%install
#disabled the documentation
make DISABLE_DOCUMENTATION=1 mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir}/btrfs install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libbtrfs.so.0*
%{_sbindir}/btrfsck
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_sbindir}/btrfs-debug-tree
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-zero-log
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-select-super

%files devel
%{_includedir}/*
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfs.a

%changelog
*   Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.10.2-2
-   Fix compilation issue againts e2fsprogs-1.44
*   Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  4.10.2-1
-   Upgrade to 4.10.2
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  4.4-1
-   Upgrade to 4.4
*   Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 3.18.2-1
-   Initial version
