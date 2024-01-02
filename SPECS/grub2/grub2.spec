%define debug_package %{nil}

Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.06
Release:    12%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
%define sha512 grub=4f11c648f3078567e53fc0c74d5026fdc6da4be27d188975e79d9a4df817ade0fe5ad2ddd694238a07edc45adfa02943d83c57767dd51548102b375e529e8efe

%ifarch x86_64
Source1: grub2-2.06~rc1-grubx64.efi.gz
%define sha512 grub2-2.06~rc1-grubx64=d7530649ee0fe5a29809850ee27dde15d977e36a784407e74bcf2a42a6f56f9b30127392771b8c188dd271408b731318abefeb2a9704b6515dbf850efb0c2763
%endif

Patch0: Tweak-grub-mkconfig.in-to-work-better-in-Photon.patch
Patch1: CVE-2022-2601-1.patch
Patch2: CVE-2022-2601-2.patch
Patch3: CVE-2022-2601-3.patch
Patch4: CVE-2022-2601-4.patch
Patch5: CVE-2022-2601-5.patch
Patch6: CVE-2022-2601-6.patch
Patch7: CVE-2022-2601-7.patch
Patch8: CVE-2022-2601-8-prep.patch
Patch9: CVE-2022-2601-8.patch
Patch10: CVE-2022-2601-9.patch
Patch11: CVE-2022-2601-10.patch
Patch12: CVE-2022-2601-11.patch
Patch13: CVE-2022-2601-12.patch
Patch14: CVE-2022-2601-13.patch
Patch15: CVE-2022-2601-14.patch
Patch16: CVE-2022-28733.patch
Patch17: CVE-2022-28734-1.patch
Patch18: CVE-2022-28734-2.patch
Patch19: CVE-2021-3695.patch
Patch20: CVE-2021-3696.patch
Patch21: CVE-2021-3697.patch
Patch22: CVE-2022-28736-prep-1.patch
Patch23: CVE-2022-28736-prep-2.patch
Patch24: CVE-2022-28736.patch

# CVE-2023-4692, CVE-2023-4693
Patch25: 0001-fs-ntfs-Fix-an-OOB-write-when-parsing-the-ATTRIBUTE_.patch
Patch26: 0002-fs-ntfs-Fix-an-OOB-read-when-reading-data-from-the-r.patch
Patch27: 0003-fs-ntfs-Fix-an-OOB-read-when-parsing-directory-entri.patch
Patch28: 0004-fs-ntfs-Fix-an-OOB-read-when-parsing-bitmaps-for-ind.patch
Patch29: 0005-fs-ntfs-Fix-an-OOB-read-when-parsing-a-volume-label.patch
Patch30: 0006-fs-ntfs-Make-code-more-readable.patch

BuildRequires:  device-mapper-devel
BuildRequires:  xz-devel
BuildRequires:  systemd-devel
BuildRequires:  bison

Requires:   xz-libs
Requires:   device-mapper-libs
Requires:   systemd-udev

%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary:    Additional language files for grub
Group:      System Environment/Programming
Requires:   %{name} = %{version}-%{release}
%description lang
These are the additional language files of grub.

%ifarch x86_64
%package pc
Summary:    GRUB Library for BIOS
Group:      System Environment/Programming
Requires:   %{name} = %{version}-%{release}
%description pc
Additional library files for grub
%endif

%package efi
Summary:    GRUB Library for UEFI
Group:      System Environment/Programming
Requires:   %{name} = %{version}-%{release}
%description efi
Additional library files for grub

%package efi-image
Summary:    GRUB UEFI image
Group:      System Environment/Base
%ifarch x86_64
Requires:   shim-signed >= 15.4
%endif
%description efi-image
GRUB UEFI image signed by vendor key

%prep
%autosetup -p1 -n grub-%{version}

%build
sh ./autogen.sh
%ifarch x86_64
mkdir -p build-for-pc
pushd build-for-pc
sh ../configure \
    --prefix=%{_prefix} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=pc \
    --target=i386 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"

make %{?_smp_mflags}

make DESTDIR=${PWD}/../install-for-pc install %{?_smp_mflags}
popd
%endif

mkdir -p build-for-efi
pushd build-for-efi
sh ../configure \
    --prefix=%{_prefix} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=efi \
    --target=%{_arch} \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"

make %{?_smp_mflags}

make DESTDIR=${PWD}/../install-for-efi install %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{_sysconfdir}/default \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}/boot/%{name}

cp -apr install-for-efi/. %{buildroot}/.
%ifarch x86_64
cp -apr install-for-pc/. %{buildroot}/.
%endif
touch %{buildroot}%{_sysconfdir}/default/grub
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
touch %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}
# Generate grub efi image
install -d %{buildroot}/boot/efi/EFI/BOOT
%ifarch x86_64
# Use presigned image from tarball as of now.
gunzip -c %{SOURCE1} > %{buildroot}/boot/efi/EFI/BOOT/grubx64.efi
# The image was created by following commands:

#cat << EOF > grub-sbat.csv
#sbat,1,SBAT Version,sbat,1,https://github.com/rhboot/shim/blob/main/SBAT.md
#grub,1,Free Software Foundation,grub,2.06~rc1,https//www.gnu.org/software/grub/
#grub.photon,1,VMware Photon OS,grub2,2.06~rc1-1.ph4,https://github.com/vmware/photon/tree/4.0/SPECS/grub2/
#EOF
#
#grub2-mkimage -d /usr/lib/grub/x86_64-efi/ -o grubx64.efi -p /boot/grub2 -O x86_64-efi --sbat=grub-sbat.csv fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm

# Local alternative:
# ./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ -o %{buildroot}/boot/efi/EFI/BOOT/grubx64.efi -p /boot/grub2 -O x86_64-efi --sbat=grub-sbat.csv fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm

%endif
%ifarch aarch64
cat > grub-embed-config.cfg << EOF
search.fs_label rootfs root
configfile /boot/grub2/grub.cfg
EOF

./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ -o %{buildroot}/boot/efi/EFI/BOOT/bootaa64.efi -p /boot/grub2 -O arm64-efi -c grub-embed-config.cfg fat iso9660 part_gpt part_msdos  normal boot linux configfile loopback chain efifwsetup efi_gop efinet ls search search_label search_fs_uuid search_fs_file  gfxterm gfxterm_background gfxterm_menu test all_video loadenv  exfat ext2 udf halt gfxmenu png tga lsefi help all_video probe echo
%endif

%if 0%{?with_check}
# make sure all files are same between two configure except the /usr/lib/grub
%check
%ifarch x86_64
diff -sr install-for-efi/sbin install-for-pc/sbin
diff -sr install-for-efi%{_bindir} install-for-pc%{_bindir}
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir}
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}
%endif
%endif

%post -p /sbin/ldconfig
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
%{_sbindir}/*
%{_bindir}/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg

%ifarch x86_64
%files pc
%defattr(-,root,root)
%{_libdir}/grub/i386-pc

%files efi
%defattr(-,root,root)
%{_libdir}/grub/x86_64-efi
%endif

%ifarch aarch64
%files efi
%defattr(-,root,root)
%{_libdir}/grub/*
%endif

%files efi-image
%defattr(-,root,root)
/boot/efi/EFI/BOOT/*

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
* Tue Jan 02 2024 Ajay Kaher <akaher@vmware.com> 2.06-12
- Fix for CVE-2021-3696
* Wed Oct 25 2023 Ajay Kaher <akaher@vmware.com> 2.06-11
- Fix for CVE-2023-4692, CVE-2023-4693
* Fri Sep 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.06-10
- Upon reconsideration additional patch to fix CVE-2022-28736 is included.
- Fixes changes made in 2.06-9
* Mon Aug 21 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.06-9
- Fix for CVE-2022-28736
* Thu Jul 20 2023 Ajay Kaher <akaher@vmware.com> 2.06-8
- Fix for CVE-2021-3697
* Thu Jul 20 2023 Ajay Kaher <akaher@vmware.com> 2.06-7
- Fix for CVE-2021-3695
* Wed Jul 19 2023 Ajay Kaher <akaher@vmware.com> 2.06-6
- Fix for CVE-2022-28734
* Wed Dec 21 2022 Ajay Kaher <akaher@vmware.com> 2.06-5
- Fix for CVE-2022-28733
* Tue Dec 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.06-4
- Fix CVE-2022-2601
* Thu Jun 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.06-3
- Add systemd-udev to Requires
* Wed Aug 18 2021 Ankit Jain <ankitja@vmware.com> 2.06-2
- Remove prompt message for default -o option
- in grub2-mkconfig
* Wed Jun 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.06-1
- Upgrade to version 2.06
* Wed Apr 28 2021 Alexey Makhalov <amakhalov@vmware.com> 2.06~rc1-2
- Update signed grubx64.efi with recent fixes and SBAT support.
* Mon Mar 15 2021 Ajay Kaher <akaher@vmware.com> 2.06~rc1-1
- upgrade to 2.06.rc1-1
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 2.04-3
- Fixes for CVE-2020-14372, CVE-2020-25632, CVE-2020-25647,
  CVE-2020-27749, CVE-2020-27779, CVE-2021-3418, CVE-2021-20225,
  CVE-2021-20233.
* Fri Oct 30 2020 Bo Gan <ganb@vmware.com> 2.04-2
- Fix boot failure on aarch64
- ERROR: (FIRMWARE BUG: efi_loaded_image_t::image_base has bogus value)
* Thu Oct 29 2020 Alexey Makhalov <amakhalov@vmware.com> 2.04-1
- Fixes for CVE-2020-10713, CVE-2020-14308, CVE-2020-14309,
  CVE-2020-14310, CVE-2020-14311, CVE-2020-15705, CVE-2020-15706
  CVE-2020-15707.
* Mon Oct 26 2020 Alexey Makhalov <amakhalov@vmware.com> 2.02-15
- Use prebuilt and presigned grubx64.efi.
* Tue Mar 10 2020 Alexey Makhalov <amakhalov@vmware.com> 2.02-14
- Package grubx64.efi (bootaa64.efi) into -efi-image subpackage.
* Wed Aug 14 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-13
- Add one more patch from fc30 to fix arm64 build.
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-12
- Update grub version from ~rc3 to release.
- Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
- Remove i386-pc modules from grub2-efi
* Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-11
- Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.02-10
- Aarch64 support
* Fri Jun 2  2017 Bo Gan <ganb@vmware.com> 2.02-9
- Split grub2 to grub2 and grub2-pc, remove grub2-efi spec
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com>  2.02-8
- Version update to 2.02~rc2
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-7
- Add fix for CVE-2015-8370
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-6
- Change systemd dependency
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.02-5
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02-4
- GA - Bump release of all rpms
* Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-3
- Adding patch to boot entries with out password.
* Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-2
- Changing program name from grub to grub2.
* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-1
- Updating grub to 2.02
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.00-1
- Initial build.  First version
