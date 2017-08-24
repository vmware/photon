Summary:	Basic system utilities
Name:		coreutils
Version:	8.27
Release:	2%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/coreutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
%define sha1 coreutils=ee054c8a4c0c924de49e4f03266733f27f986fbb
Patch0:		http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.27-i18n-1.patch
Patch1:		http://www.linuxfromscratch.org/patches/downloads/coreutils/coreutils-8.27-uname-1.patch
Requires:	gmp
Provides:	sh-utils
%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary: Additional language files for coreutils
Group: System Environment/Base
Requires: coreutils >= %{version}
%description lang
These are the additional language files of coreutils.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%build
export FORCE_UNSAFE_CONFIGURE=1 &&  ./configure \
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
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
#make NON_ROOT_USERNAME=nobody check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

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
*       Wed Aug 09 2017 Rongrong Qiu <rqiu@vmware.com> 8.27-2
-       Fix make check for bug 1900253
*       Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 8.27-1
-       Upgraded to version 8.27
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.25-2
-	GA - Bump release of all rpms
*	Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 8.25-1
- 	Updated to version 8.25
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 8.24-1
- 	Updated to version 8.24
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 8.22-1
-	Initial build. First version
