Summary:	Program for compiling packages
Name:		make
Version:	4.3
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/make
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.gz
%define sha1 make=3c40e5b49b893dbb14f1e2e1f8fe89b7298cc51d
%description
The Make package contains a program for compiling packages.
%prep
%setup -q
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
*	Mon May 03 2021 Ajay Kaher <akaher@vmware.com> 4.3-1
-	Update to version 4.3
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1-3
-	GA - Bump release of all rpms
*       Tue May 10 2016 Kumar Kaushik <kaushikk@vmware.com>  4.1-2
-       Fix for segfaults in chroot env.
*       Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  4.1-1
-       Update version.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.0-1
-	Initial build.	First version
