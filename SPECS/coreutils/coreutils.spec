Summary:	Basic system utilities
Name:		coreutils
Version:	8.22
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/coreutils
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
%define sha1 coreutils=cc7fe47b21eb49dd2ee4cdb707570f42fb2c8cc6
Patch0:		http://www.linuxfromscratch.org/patches/lfs/7.5/coreutils-8.22-i18n-4.patch
Requires:	gmp
%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary: Additional language files for coreutils
Group: System Environment/Base
Requires: coreutils >= 8.22
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
make -k NON_ROOT_USERNAME=nobody check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 8.22-1
-	Initial build. First version
