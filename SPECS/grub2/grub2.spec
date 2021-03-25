%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.06~rc1
Release:    1%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    ftp://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
%define sha1 grub=7cb2eb385c222e798b279174c9f717ddbe7d4608
Source1:    gnulib-d271f868a.tar.xz
%define sha1 gnulib=bfaa70d4657b653e01716e917576f6c4a4aa2126

Patch225:   0225-update-safemath-with-fallback-code-for-gcc-older-tha.patch

# Other security enhancement
Patch301:   0067-Fix-security-issue-when-reading-username-and-passwor.patch
Patch302:   0224-Rework-how-the-fdt-command-builds.patch

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

%patch225 -p1

%patch301 -p1
%patch302 -p1

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
*   Mon Mar 15 2021 Ajay Kaher <akaher@vmware.com> 2.06~rc1-1
-   upgrade to 2.06~rc1-1
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
