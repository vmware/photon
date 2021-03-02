%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.04
Release:    3%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    ftp://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
%define sha1 grub=3ed21de7be5970d7638b9f526bca3292af78e0fc
%ifarch x86_64
Source1:    grub2-2.02-grubx64.efi.gz
%define sha1 grub2-2.02-grubx64=32d5ee61df1256152ba13b7d629eac67e0f3a911
%endif
# Includes fixes for
# CVE-2020-10713 (BootHole) and co:
# CVE-2020-14308, CVE-2020-14309, CVE-2020-14310, CVE-2020-14311,
# CVE-2020-15706, CVE-2020-15707.
# ACPI Hole and co:
# CVE-2020-14372, CVE-2020-25632, CVE-2020-25647, CVE-2020-27749,
# CVE-2020-27779, CVE-2021-3418, CVE-2021-20225, CVE-2021-20233.
Patch0:     release-to-master.patch
# New commits in release-to-master (such as luks2) require
# re-bootstraping of gnulib. As it figured out only missing
# piece in grub's gnulib version is base64 support.
# Instead of providing external gnulib tarbal, just patch
# current one.
Patch1:     gnulib-add-base64.patch

# Other security enhancement
Patch307:   0067-Fix-security-issue-when-reading-username-and-passwor.patch

BuildRequires:  device-mapper-devel
BuildRequires:  xz-devel
BuildRequires:  systemd-devel
Requires:   xz
Requires:   device-mapper
%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary: Additional language files for grub
Group: System Environment/Programming
Requires: %{name} = %{version}
%description lang
These are the additional language files of grub.

%ifarch x86_64
%package pc
Summary: GRUB Library for BIOS
Group: System Environment/Programming
Requires: %{name} = %{version}
%description pc
Additional library files for grub
%endif

%package efi
Summary: GRUB Library for UEFI
Group: System Environment/Programming
Requires: %{name} = %{version}
%description efi
Additional library files for grub

%package efi-image
Summary: GRUB UEFI image
Group: System Environment/Base
%ifarch x86_64
Requires: shim-signed
%endif
%description efi-image
GRUB UEFI image signed by vendor key

%prep
%setup -qn grub-%{version}
%patch0 -p1
%patch1 -p1
%patch307 -p1

%build
./autogen.sh
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=pc \
    --target=i386 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-pc install
popd
%endif

mkdir build-for-efi
pushd build-for-efi
../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=efi \
    --target=%{_arch} \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-efi install
popd

# make sure all files are same between two configure except the /usr/lib/grub
%check
%ifarch x86_64
diff -sr install-for-efi/sbin install-for-pc/sbin && \
diff -sr install-for-efi%{_bindir} install-for-pc%{_bindir} && \
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir} && \
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}
%endif

%install
mkdir -p %{buildroot}
cp -a install-for-efi/. %{buildroot}/.
%ifarch x86_64
cp -a install-for-pc/. %{buildroot}/.
%endif
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
mkdir -p %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}
# Generate grub efi image
install -d %{buildroot}/boot/efi/EFI/BOOT
%ifarch x86_64
# Use presigned image from tarball as of now.
gunzip -c %{SOURCE1} > %{buildroot}/boot/efi/EFI/BOOT/grubx64.efi
# ./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ -o %{buildroot}/boot/efi/EFI/BOOT/grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm

%endif
%ifarch aarch64
cat > grub-embed-config.cfg << EOF
search.fs_label rootfs root
configfile /boot/grub2/grub.cfg
EOF

./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ -o %{buildroot}/boot/efi/EFI/BOOT/bootaa64.efi -p /boot/grub2 -O arm64-efi -c grub-embed-config.cfg fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain efifwsetup efi_gop efinet ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help all_video probe echo
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/grub.d
%config() %{_sysconfdir}/bash_completion.d/grub
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/30_uefi-firmware
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg

%ifarch x86_64
%files pc
%{_libdir}/grub/i386-pc
%files efi
%{_libdir}/grub/x86_64-efi
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%files efi-image
/boot/efi/EFI/BOOT/*

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
*   Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 2.04-3
-   Fixes for CVE-2020-14372, CVE-2020-25632, CVE-2020-25647,
    CVE-2020-27749, CVE-2020-27779, CVE-2021-3418, CVE-2021-20225,
    CVE-2021-20233.
*   Fri Oct 30 2020 Bo Gan <ganb@vmware.com> 2.04-2
-   Fix boot failure on aarch64
-   ERROR: (FIRMWARE BUG: efi_loaded_image_t::image_base has bogus value)
*   Thu Oct 29 2020 Alexey Makhalov <amakhalov@vmware.com> 2.04-1
-   Fixes for CVE-2020-10713, CVE-2020-14308, CVE-2020-14309,
    CVE-2020-14310, CVE-2020-14311, CVE-2020-15705, CVE-2020-15706
    CVE-2020-15707.
*   Mon Oct 26 2020 Alexey Makhalov <amakhalov@vmware.com> 2.02-15
-   Use prebuilt and presigned grubx64.efi.
*   Tue Mar 10 2020 Alexey Makhalov <amakhalov@vmware.com> 2.02-14
-   Package grubx64.efi (bootaa64.efi) into -efi-image subpackage.
*   Wed Aug 14 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-13
-   Add one more patch from fc30 to fix arm64 build.
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-12
-   Update grub version from ~rc3 to release.
-   Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
-   Remove i386-pc modules from grub2-efi
*   Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-11
-   Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.02-10
-   Aarch64 support
*   Fri Jun 2  2017 Bo Gan <ganb@vmware.com> 2.02-9
-   Split grub2 to grub2 and grub2-pc, remove grub2-efi spec
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com>  2.02-8
-   Version update to 2.02~rc2
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-7
-   Add fix for CVE-2015-8370
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-6
-   Change systemd dependency
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.02-5
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02-4
-   GA - Bump release of all rpms
*   Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-3
-   Adding patch to boot entries with out password.
*   Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-2
-   Changing program name from grub to grub2.
*   Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-1
-   Updating grub to 2.02
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.00-1
-   Initial build.  First version
