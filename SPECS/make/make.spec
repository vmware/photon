Summary:	Program for compiling packages
Name:		make
Version:	4.1
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/make
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Patch0:         chroot-segfault-fix.patch
Source0:	http://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2
%define sha1 make=0d701882fd6fd61a9652cb8d866ad7fc7de54d58
%description
The Make package contains a program for compiling packages.
%prep
%setup -q
%patch0 -p1
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gnumake.h
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	4.1-3
-	GA - Bump release of all rpms
*       Tue May 10 2016 Kumar Kaushik <kaushikk@vmware.com>  4.1-2
-       Fix for segfaults in chroot env.
*       Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  4.1-1
-       Update version.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.0-1
-	Initial build.	First version
