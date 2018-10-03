Name:       btrfs-progs
Version:    4.17.1
Release:    1%{?dist}
Summary:    Userspace programs for btrfs
Group:      System Environment/Base
License:    GPLv2+
URL:        http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:    http://ftp.ntu.edu.tw/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
%define sha1 btrfs-progs=6be18f21eb6cd00f9826c598f5a482e9be2eb9b2
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  lzo-devel
BuildRequires:  e2fsprogs-devel,libacl-devel
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  zstd-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
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
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-select-super

%files devel
%{_includedir}/*
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfs.a
%{_libdir}/libbtrfsutil.*

%changelog
*   Wed Oct 03 2018 Sujay G <gsujay@vmware.com> 4.17.1-1
-   Bump btrfs-progs version to 4.17.1
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
