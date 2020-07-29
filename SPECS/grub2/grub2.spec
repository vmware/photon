%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.04
Release:    1%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    ftp://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
%define sha1 grub=3ed21de7be5970d7638b9f526bca3292af78e0fc
Patch0:     release-to-master.patch
# New commits in release-to-master (such as luks2) require
# re-bootstraping of gnulib. As it figured out only missing
# piece in grub's gnulib version is base64 support.
# Instead of providing external gnulib tarbal, just patch
# current one.
Patch1:     gnulib-add-base64.patch
# Fixes for CVE-2020-10713 and co:
# CVE-2020-14308, CVE-2020-14309, CVE-2020-14310, CVE-2020-14311,
# CVE-2020-15706, CVE-2020-15707.
Patch200:   0200-yylex-Make-lexer-fatal-errors-actually-be-fatal.patch
Patch201:   0201-safemath-Add-some-arithmetic-primitives-that-check-f.patch
Patch202:   0202-calloc-Make-sure-we-always-have-an-overflow-checking.patch
Patch203:   0203-calloc-Use-calloc-at-most-places.patch
Patch204:   0204-malloc-Use-overflow-checking-primitives-where-we-do-.patch
Patch205:   0205-iso9660-Don-t-leak-memory-on-realloc-failures.patch
Patch206:   0206-font-Do-not-load-more-than-one-NAME-section.patch
Patch207:   0207-gfxmenu-Fix-double-free-in-load_image.patch
Patch208:   0208-xnu-Fix-double-free-in-grub_xnu_devprop_add_property.patch
Patch209:   0209-json-Avoid-a-double-free-when-parsing-fails.patch
Patch210:   0210-lzma-Make-sure-we-don-t-dereference-past-array.patch
Patch211:   0211-term-Fix-overflow-on-user-inputs.patch
Patch212:   0212-udf-Fix-memory-leak.patch
Patch213:   0213-multiboot2-Fix-memory-leak-if-grub_create_loader_cmd.patch
Patch214:   0214-tftp-Do-not-use-priority-queue.patch
Patch215:   0215-relocator-Protect-grub_relocator_alloc_chunk_addr-in.patch
Patch216:   0216-relocator-Protect-grub_relocator_alloc_chunk_align-m.patch
Patch217:   0217-script-Remove-unused-fields-from-grub_script_functio.patch
Patch218:   0218-script-Avoid-a-use-after-free-when-redefining-a-func.patch
Patch219:   0219-relocator-Fix-grub_relocator_alloc_chunk_align-top-m.patch
Patch220:   0220-hfsplus-fix-two-more-overflows.patch
Patch221:   0221-lvm-fix-two-more-potential-data-dependent-alloc-over.patch
Patch222:   0222-emu-make-grub_free-NULL-safe.patch
Patch223:   0223-efi-fix-some-malformed-device-path-arithmetic-errors.patch
Patch224:   0224-Fix-a-regression-caused-by-efi-fix-some-malformed-de.patch
Patch225:   0225-update-safemath-with-fallback-code-for-gcc-older-tha.patch
Patch226:   0226-efi-Fix-use-after-free-in-halt-reboot-path.patch
Patch227:   0227-linux-loader-avoid-overflow-on-initrd-size-calculati.patch
Patch228:   0228-linux-Fix-integer-overflows-in-initrd-size-handling.patch

# Set of Secure Boot enforcement patches
Patch300:   0001-Add-support-for-Linux-EFI-stub-loading.patch
Patch301:   0002-Rework-linux-command.patch
Patch302:   0003-Rework-linux16-command.patch
Patch303:   0004-Add-secureboot-support-on-efi-chainloader.patch
Patch304:   0005-Make-any-of-the-loaders-that-link-in-efi-mode-honor-.patch
Patch305:   0006-Handle-multi-arch-64-on-32-boot-in-linuxefi-loader.patch
# Fix CVE-2020-15705
Patch306:   0007-linuxefi-fail-kernel-validation-without-shim-protoco.patch
# Other security enhancement
Patch307:   0067-Fix-security-issue-when-reading-username-and-passwor.patch
Patch308:   0224-Rework-how-the-fdt-command-builds.patch

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

%package pc
Summary: GRUB Library for BIOS
Group: System Environment/Programming
Requires: %{name} = %{version}
%description pc
Additional library files for grub

%package efi
Summary: GRUB Library for UEFI
Group: System Environment/Programming
Requires: %{name} = %{version}
%description efi
Additional library files for grub

%prep
%setup -qn grub-%{version}
%patch0 -p1
%patch1 -p1
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch210 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch218 -p1
%patch219 -p1
%patch220 -p1
%patch221 -p1
%patch222 -p1
%patch223 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch300 -p1
%patch301 -p1
%patch302 -p1
%patch303 -p1
%patch304 -p1
%patch305 -p1
%patch306 -p1
%patch307 -p1
%patch308 -p1

%build
./autogen.sh
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
    --target=x86_64 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-efi install
popd

# make sure all files are same between two configure except the /usr/lib/grub
%check
diff -sr install-for-efi/sbin install-for-pc/sbin && \
diff -sr install-for-efi%{_bindir} install-for-pc%{_bindir} && \
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir} && \
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}

%install
mkdir -p %{buildroot}
cp -a install-for-efi/. %{buildroot}/.
cp -a install-for-pc/. %{buildroot}/.
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
mkdir -p %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

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

%files pc
%{_libdir}/grub/i386-pc

%files efi
%{_libdir}/grub/x86_64-efi

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
*   Tue Jul 21 2020 Alexey Makhalov <amakhalov@vmware.com> 2.04-1
-   Fixes for CVE-2020-10713, CVE-2020-14308, CVE-2020-14309,
    CVE-2020-14310, CVE-2020-14311, CVE-2020-15705, CVE-2020-15706
    CVE-2020-15707.
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
