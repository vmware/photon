%global security_hardening none
Summary:	Simple kernel loader which boots from a FAT filesystem
Name:		syslinux
Version:	6.04
Release:	3%{?dist}
License:	GPLv2+
URL:		http://www.syslinux.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.kernel.org/pub/linux/utils/boot/%{name}/Testing/%{version}/%{name}-%{version}-pre1.tar.xz
Patch0:		0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
BuildRequires:	nasm
BuildRequires:	util-linux-devel
Requires:	util-linux

%define sha1 syslinux=599b7a85d522b1b6658a1fe290e4d23dc64b1470
%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package devel
Summary: Headers and libraries for syslinux development.
Group: Development/Libraries
Provides: %{name}-static = %{version}-%{release}
%description devel
Headers and libraries for syslinux development.

%prep
%setup -q -n %{name}-%{version}-pre1
%patch0 -p1
%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' extlinux/main.c
make bios clean all
%install
make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32
rm -rf %{buildroot}/boot
rm -rf %{buildroot}/tftpboot
# remove it unless provide perl(Crypt::PasswdMD5)
rm %{buildroot}/%{_bindir}/md5pass
# remove it unless provide perl(Digest::SHA1)
rm %{buildroot}/%{_bindir}/sha1pass
%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %{_datadir}/syslinux/com32
%exclude %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_datadir}/syslinux/com32/*

%changelog
*   Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 6.04-3
-   Fix compilation issue against glibc-2.28
*   Wed Oct 25 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-2
-   Remove md5pass and sha1pass tools
*   Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-1
-   Initial version
