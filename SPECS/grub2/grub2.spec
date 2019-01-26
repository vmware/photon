%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.02
Release:    11%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://alpha.gnu.org/gnu/grub/grub-2.02~rc2.tar.xz
%define sha1 grub=4f6f3719fd7dbb0449a58547c1b08c9801337663
Patch0:     Fix_to_boot_entries_with_out_password.patch
Patch1:     0001-Secure-Boot-support.patch
%ifarch aarch64
Patch100:   0001-efinet-do-not-start-EFI-networking-at-module-init-ti.patch
%endif
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

%prep
%setup -qn grub-2.02~rc2
%patch0 -p1
%patch1 -p1
%ifarch aarch64
%patch100 -p1
%endif
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

#make sure all the files are same between two configure except the /usr/lib/grub
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
%endif

%files efi
%{_libdir}/grub/*

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
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
