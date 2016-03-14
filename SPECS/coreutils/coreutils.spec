Summary:	Basic system utilities
Name:		coreutils
Version:	8.24
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/coreutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
%define sha1 coreutils=cf3d9983461c2b0c074a76804c18464e9a474883
Patch0:		http://http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.24-i18n-1.patch
Requires:	gmp
Provides:	sh-utils
%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary: Additional language files for coreutils
Group: System Environment/Base
Requires: coreutils >= 8.24
%description lang
These are the additional language files of coreutils.

%prep
%setup -q
%patch0 -p1
%build
FORCE_UNSAFE_CONFIGURE=1  ./configure \
	--prefix=%{_prefix} \
	--enable-no-install-program=kill,uptime \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{false,ln,ls,mkdir,mknod,mv,pwd,rm} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/{rmdir,stty,sync,true,uname,test,[} %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i s/\"1\"/\"8\"/1 %{buildroot}%{_mandir}/man8/chroot.8
mv -v %{buildroot}%{_bindir}/{head,sleep,nice} %{buildroot}/bin
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
make NON_ROOT_USERNAME=nobody check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
/bin/*
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 8.24-1
- 	Updated to version 8.24
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 8.22-1
-	Initial build. First version
