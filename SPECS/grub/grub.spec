Summary:	GRand Unified Bootloader
Name:		grub
Version:	2.00
Release:	1
License:	GPLv3+
URL:		http://www.gnu.org/software/grub
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/grub/%{name}-%{version}.tar.xz
%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary: Additional language files for grub
Group: System Environment/Programming
Requires: grub >= 2.00
%description lang
These are the additional language files of grub.


%prep
%setup -q
sed -i -e '/gets is a/d' grub-core/gnulib/stdio.in.h
%build
./configure \
	--prefix=%{_prefix} \
	--sbindir=/sbin \
	--sysconfdir=%{_sysconfdir} \
	--disable-grub-emu-usb \
	--disable-efiemu \
	--disable-werror 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%dir %{_sysconfdir}/grub.d
%config() %{_sysconfdir}/bash_completion.d/grub
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/40_custom
%config() %{_sysconfdir}/grub.d/41_custom
%config() %{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_libdir}/grub/*
%{_datarootdir}/%{name}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.00-1
-	Initial build.	First version
