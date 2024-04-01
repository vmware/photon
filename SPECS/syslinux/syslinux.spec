%global security_hardening none
%define zlibver 1.2.13
%define libpngver 1.6.39

Summary:      Simple kernel loader which boots from a FAT filesystem
Name:         syslinux
Version:      6.04
Release:      11%{?dist}
License:      GPLv2+
URL:          http://www.syslinux.org
Group:        Applications/System
Vendor:       VMware, Inc.
Distribution: Photon

Source0:    https://www.kernel.org/pub/linux/utils/boot/%{name}/Testing/%{version}/%{name}-%{version}-pre1.tar.xz
%define sha512  %{name}=7927dd39be8e2dcf4138a6fea33def67d19d938379d694f15b48fdd2f5924c028b7a9e7bd71d0c7c6630c203e9e2a54296628e530632ad5e6f55b1ebefe8fc98

Source1:        https://sourceforge.net/projects/libpng/files/libpng16/%{libpngver}/libpng-%{libpngver}.tar.xz
%define sha512  libpng=ce233bb58d70b391b7dc858a132a8f9f66a9e30f5b387426317fdd5e76e8395e00ec36324e5e2caec8fda49a3f2b13fe27594a3466fdf2020ec7520e79a608c9

Source2:        https://www.zlib.net/zlib-%{zlibver}.tar.gz
%define sha512  zlib=99f0e843f52290e6950cc328820c0f322a4d934a504f66c7caa76bd0cc17ece4bf0546424fc95135de85a2656fed5115abb835fd8d8a390d60ffaf946c8887ad

Patch0:     0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
Patch1:     syslinux-6.04_pre1-fcommon.patch
Patch2:     0006-Replace-builtin-strlen-that-appears-to-get-optimized.patch
Patch3:     0001-zlib-update-to-version-1.2.11.patch
Patch4:     0001-libpng-update-to-1.6.36.patch

BuildArch:      x86_64

BuildRequires:  nasm
BuildRequires:  util-linux-devel

Requires:   util-linux

%description
SYSLINUX is a suite of bootloaders, currently supporting DOS FAT
filesystems, Linux ext2/ext3 filesystems (EXTLINUX), PXE network boots
(PXELINUX), or ISO 9660 CD-ROMs (ISOLINUX).  It also includes a tool,
MEMDISK, which loads legacy operating systems from these media.

%package devel
Summary:    Headers and libraries for syslinux development.
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-static = %{version}-%{release}
%description devel
Headers and libraries for syslinux development.

%prep
%autosetup -p1 -n %{name}-%{version}-pre1

# to have higher versions of libpng, zlib
rm -rf com32/lib/libpng/ com32/lib/zlib/
tar xf %{SOURCE1} -C com32/lib/
tar xf %{SOURCE2} -C com32/lib/
mv com32/lib/libpng-%{libpngver} com32/lib/libpng
mv com32/lib/zlib-%{zlibver} com32/lib/zlib

%build
#make some fixes required by glibc-2.28:
sed -i '/unistd/a #include <sys/sysmacros.h>' extlinux/main.c
# make doesn't support _smp_mflags
make bios clean all

%install
# make doesn't support _smp_mflags
make bios install-all \
    INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
    LIBDIR=%{_libdir} DATADIR=%{_datadir} \
    MANDIR=%{_mandir} INCDIR=%{_includedir} \
    LDLINUX=ldlinux.c32

rm -rf %{buildroot}/boot \
       %{buildroot}/tftpboot
# remove it unless provide perl(Crypt::PasswdMD5)
rm %{buildroot}%{_bindir}/md5pass
# remove it unless provide perl(Digest::SHA1)
rm %{buildroot}%{_bindir}/sha1pass

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %dir %{_datadir}/%{name}/com32
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_datadir}/%{name}/com32/*

%changelog
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.04-11
- Bump version as a part of util-linux upgrade
* Fri Jun 16 2023 Srish Srinivasan <ssrish@vmware.com> 6.04-10
- Update libpng and zlib source to the latest versions to fix multiple CVEs
* Mon Apr 17 2023 Nitesh Kumar <kunitesh@vmware.com> 6.04-9
- Bump version as a part of nasm v2.16.01 upgrade
* Mon Jul 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.04-8
- Fix devel requires
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.04-7
- Fix binary path
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 6.04-6
- GCC-10 support.
* Tue Jun 04 2019 Ajay Kaher <akaher@vmware.com> 6.04-5
- Upgrade zlib to v1.2.11 and libpng to v1.2.59
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 6.04-4
- Adding BuildArch
* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 6.04-3
- Fix compilation issue against glibc-2.28
* Wed Oct 25 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-2
- Remove md5pass and sha1pass tools
* Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 6.04-1
- Initial version
